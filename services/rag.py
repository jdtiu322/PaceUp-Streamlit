from __future__ import annotations

import json
import logging
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL


logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
RAG_INDEX_PATH = REPO_ROOT / "data" / "rag_index.json"
RAG_EMBEDDINGS_PATH = REPO_ROOT / "data" / "rag_embeddings.json"
DEFAULT_TOP_K = 5

TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
STOP_WORDS = {
    "a",
    "about",
    "after",
    "am",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "but",
    "can",
    "do",
    "for",
    "from",
    "give",
    "help",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "what",
    "when",
    "with",
}

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_rag_index() -> dict[str, Any]:
    return _load_json(RAG_INDEX_PATH)


@lru_cache(maxsize=1)
def load_rag_embeddings() -> dict[str, Any]:
    return _load_json(RAG_EMBEDDINGS_PATH)


def refresh_rag_cache() -> None:
    load_rag_index.cache_clear()
    load_rag_embeddings.cache_clear()


def _chunks_from_embeddings() -> list[dict[str, Any]]:
    data = load_rag_embeddings()
    chunks = data.get("chunks", [])
    if not chunks:
        return []

    model = data.get("embedding_model")
    if model and model != GEMINI_EMBEDDING_MODEL:
        logger.warning(
            "RAG embedding model mismatch: file uses %s, config uses %s.",
            model,
            GEMINI_EMBEDDING_MODEL,
        )
    return chunks


def _chunks_from_index() -> list[dict[str, Any]]:
    return load_rag_index().get("chunks", [])


def _tokenize(text: str) -> list[str]:
    tokens = [token.casefold() for token in TOKEN_RE.findall(text or "")]
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def _extract_embedding(response: Any) -> list[float]:
    embeddings = getattr(response, "embeddings", None) or []
    if not embeddings:
        return []

    values = getattr(embeddings[0], "values", None)
    return [float(value) for value in values] if values else []


def embed_query(query: str) -> list[float]:
    if client is None:
        return []

    response = client.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=[query],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return _extract_embedding(response)


def _lexical_score(query_tokens: list[str], chunk: dict[str, Any]) -> float:
    if not query_tokens:
        return 0.0

    text = " ".join(
        str(chunk.get(field, ""))
        for field in ("document_title", "heading", "source", "text")
    )
    chunk_tokens = _tokenize(text)
    if not chunk_tokens:
        return 0.0

    query_set = set(query_tokens)
    chunk_set = set(chunk_tokens)
    overlap = query_set & chunk_set
    if not overlap:
        return 0.0

    score = len(overlap) / math.sqrt(len(query_set) * len(chunk_set))

    heading_tokens = set(_tokenize(str(chunk.get("heading", ""))))
    title_tokens = set(_tokenize(str(chunk.get("document_title", ""))))
    score += 0.12 * len(overlap & heading_tokens)
    score += 0.08 * len(overlap & title_tokens)

    query_text = " ".join(query_tokens)
    evidence_terms = {"study", "studies", "evidence", "research", "source", "citation"}
    if query_set & evidence_terms and chunk.get("layer") == "evidence":
        score += 0.12
    if "race" in query_set and "race" in str(chunk.get("source", "")).casefold():
        score += 0.08
    if query_text and query_text in str(chunk.get("text", "")).casefold():
        score += 0.2

    return score


def _public_chunk(
    chunk: dict[str, Any],
    *,
    score: float,
    retrieval_strategy: str,
) -> dict[str, Any]:
    public = {
        key: chunk.get(key)
        for key in (
            "id",
            "layer",
            "source",
            "source_path",
            "document_title",
            "heading",
            "text",
            "word_count",
            "citations",
        )
    }
    public["score"] = round(float(score), 6)
    public["retrieval_strategy"] = retrieval_strategy
    return public


def retrieve_context(
    query: str,
    *,
    top_k: int = DEFAULT_TOP_K,
    min_score: float = 0.0,
    prefer_embeddings: bool = True,
) -> list[dict[str, Any]]:
    query = (query or "").strip()
    if not query or top_k <= 0:
        return []

    if prefer_embeddings:
        embedded_chunks = [
            chunk for chunk in _chunks_from_embeddings() if chunk.get("embedding")
        ]
        if embedded_chunks:
            try:
                query_embedding = embed_query(query)
                if query_embedding:
                    scored = [
                        (
                            _cosine_similarity(query_embedding, chunk["embedding"]),
                            chunk,
                        )
                        for chunk in embedded_chunks
                    ]
                    return [
                        _public_chunk(
                            chunk,
                            score=score,
                            retrieval_strategy="embedding",
                        )
                        for score, chunk in sorted(
                            scored,
                            key=lambda item: item[0],
                            reverse=True,
                        )
                        if score > min_score
                    ][:top_k]
            except Exception:
                logger.exception("Embedding RAG retrieval failed; using lexical fallback.")

    query_tokens = _tokenize(query)
    scored = [
        (_lexical_score(query_tokens, chunk), chunk) for chunk in _chunks_from_index()
    ]
    return [
        _public_chunk(chunk, score=score, retrieval_strategy="lexical")
        for score, chunk in sorted(scored, key=lambda item: item[0], reverse=True)
        if score >= min_score and score > 0
    ][:top_k]


def format_rag_context(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return ""

    formatted_chunks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        header = (
            f"[RAG-{index}] {chunk.get('heading')} "
            f"({chunk.get('layer')} / {chunk.get('source')})"
        )
        lines = [header, str(chunk.get("text", "")).strip()]

        citations = chunk.get("citations") or []
        for citation in citations[:2]:
            title = citation.get("title", "Untitled source")
            year = citation.get("year")
            url = citation.get("url")
            source_text = f"Source: {title}"
            if year:
                source_text += f" ({year})"
            if url:
                source_text += f" - {url}"
            lines.append(source_text)

        formatted_chunks.append("\n".join(line for line in lines if line))

    return "\n\n".join(formatted_chunks)
