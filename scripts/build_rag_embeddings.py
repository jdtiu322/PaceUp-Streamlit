from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / "data" / "rag_index.json"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "rag_embeddings.json"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing input file: {repo_relative(path)}")
    return json.loads(path.read_text(encoding="utf-8"))


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def existing_embeddings(path: Path, model: str) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}

    data = load_json(path)
    if data.get("embedding_model") != model:
        return {}

    by_id: dict[str, dict[str, Any]] = {}
    for chunk in data.get("chunks", []):
        chunk_id = chunk.get("id")
        embedding = chunk.get("embedding")
        fingerprint = chunk.get("text_sha256")
        if chunk_id and embedding and fingerprint:
            by_id[chunk_id] = chunk
    return by_id


def extract_embedding(response: Any) -> list[float]:
    embeddings = getattr(response, "embeddings", None) or []
    if not embeddings:
        raise RuntimeError("Embedding response did not include embeddings.")

    values = getattr(embeddings[0], "values", None)
    if not values:
        raise RuntimeError("Embedding response did not include vector values.")

    return [float(value) for value in values]


def embed_document(
    client: genai.Client,
    *,
    model: str,
    text: str,
    title: str,
    output_dimensionality: int | None,
) -> list[float]:
    config: dict[str, Any] = {
        "task_type": "RETRIEVAL_DOCUMENT",
        "title": title[:256],
    }
    if output_dimensionality:
        config["output_dimensionality"] = output_dimensionality

    response = client.models.embed_content(
        model=model,
        contents=[text],
        config=types.EmbedContentConfig(**config),
    )
    return extract_embedding(response)


def build_embeddings(
    *,
    index_path: Path,
    output_path: Path,
    api_key: str,
    model: str,
    output_dimensionality: int | None,
    sleep_seconds: float,
    force: bool,
) -> dict[str, Any]:
    index = load_json(index_path)
    chunks = index.get("chunks", [])
    if not chunks:
        raise SystemExit("No chunks found in the RAG index.")

    reusable = {} if force else existing_embeddings(output_path, model)
    client = genai.Client(api_key=api_key)
    embedded_chunks: list[dict[str, Any]] = []

    for position, chunk in enumerate(chunks, start=1):
        chunk_id = str(chunk["id"])
        fingerprint = text_hash(str(chunk["text"]))
        previous = reusable.get(chunk_id)

        if previous and previous.get("text_sha256") == fingerprint:
            embedded_chunks.append(previous)
            print(f"[{position}/{len(chunks)}] reused {chunk_id}")
            continue

        title = f"{chunk.get('document_title', '')}: {chunk.get('heading', '')}".strip(": ")
        embedding = embed_document(
            client,
            model=model,
            text=str(chunk["text"]),
            title=title or chunk_id,
            output_dimensionality=output_dimensionality,
        )
        embedded_chunk = {
            **chunk,
            "embedding": embedding,
            "embedding_dim": len(embedding),
            "embedding_model": model,
            "text_sha256": fingerprint,
        }
        embedded_chunks.append(embedded_chunk)
        print(f"[{position}/{len(chunks)}] embedded {chunk_id} ({len(embedding)} dims)")

        if sleep_seconds:
            time.sleep(sleep_seconds)

    embedding_dims = sorted({chunk["embedding_dim"] for chunk in embedded_chunks})
    output = {
        "embedding_index_version": 1,
        "source_index_path": repo_relative(index_path),
        "source_index_version": index.get("index_version"),
        "source_index_chunk_count": index.get("chunk_count"),
        "embedding_model": model,
        "embedding_dims": embedding_dims,
        "chunk_count": len(embedded_chunks),
        "chunks": embedded_chunks,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Gemini embeddings for the local PaceUp RAG index."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Input RAG index path. Defaults to data/rag_index.json.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output embeddings path. Defaults to data/rag_embeddings.json.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        help="Gemini embedding model. Defaults to GEMINI_EMBEDDING_MODEL or gemini-embedding-001.",
    )
    parser.add_argument(
        "--output-dimensionality",
        type=int,
        default=None,
        help="Optional reduced embedding dimensionality for supported models.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep between embedding requests.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild every embedding instead of reusing unchanged chunks.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv(REPO_ROOT / ".env")
    args = parse_args()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Missing GEMINI_API_KEY. Add it to .env or the environment.")

    index_path = args.index if args.index.is_absolute() else REPO_ROOT / args.index
    output_path = args.output if args.output.is_absolute() else REPO_ROOT / args.output

    output = build_embeddings(
        index_path=index_path,
        output_path=output_path,
        api_key=api_key,
        model=args.model,
        output_dimensionality=args.output_dimensionality,
        sleep_seconds=args.sleep,
        force=args.force,
    )
    print(
        f"Wrote {output['chunk_count']} embedded chunks to {repo_relative(output_path)} "
        f"using {output['embedding_model']}"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted.")
