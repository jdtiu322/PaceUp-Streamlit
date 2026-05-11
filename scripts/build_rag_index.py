from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "rag_index.json"
SOURCE_DIRS = (
    ("knowledge", REPO_ROOT / "data" / "knowledge"),
    ("evidence", REPO_ROOT / "data" / "evidence"),
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LABEL_RE = re.compile(r"^(Evidence summary|Practical PaceUp use|Citation):\s*$")
FIELD_RE = re.compile(r"^-\s+([^:]+):\s*(.*)$")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "untitled"


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def clean_lines(lines: Iterable[str]) -> str:
    text = "\n".join(line.rstrip() for line in lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def markdown_files(root: Path, include_readme: bool) -> list[Path]:
    if not root.exists():
        return []

    files = sorted(root.glob("*.md"), key=lambda path: path.name.lower())
    if include_readme:
        return files
    return [path for path in files if path.name.lower() != "readme.md"]


def split_sections(markdown: str) -> tuple[str, list[dict[str, str]]]:
    title = "Untitled"
    sections: list[dict[str, str]] = []
    active_heading: str | None = None
    active_lines: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        heading_match = HEADING_RE.match(line)

        if heading_match:
            level = len(heading_match.group(1))
            heading = heading_match.group(2).strip()

            if level == 1:
                title = heading
                continue

            if level == 2:
                if active_heading is not None:
                    sections.append(
                        {
                            "heading": active_heading,
                            "body": clean_lines(active_lines),
                        }
                    )
                active_heading = heading
                active_lines = []
                continue

        if active_heading is not None:
            active_lines.append(line)

    if active_heading is not None:
        sections.append({"heading": active_heading, "body": clean_lines(active_lines)})

    if not sections:
        body = clean_lines(
            line for line in markdown.splitlines() if not line.lstrip().startswith("#")
        )
        if body:
            sections.append({"heading": title, "body": body})

    return title, [section for section in sections if section["body"]]


def extract_labeled_blocks(body: str) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {
        "Evidence summary": [],
        "Practical PaceUp use": [],
        "Citation": [],
    }
    active_label: str | None = None

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        label_match = LABEL_RE.match(line)
        if label_match:
            active_label = label_match.group(1)
            continue

        if active_label:
            blocks[active_label].append(line)

    return {label: lines for label, lines in blocks.items() if clean_lines(lines)}


def normalize_field_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    return {
        "doi": "doi",
        "url": "url",
        "pmid": "pmid",
    }.get(normalized, normalized)


def parse_citations(lines: list[str]) -> list[dict[str, str]]:
    citations: list[dict[str, str]] = []
    current: dict[str, str] = {}

    for line in lines:
        match = FIELD_RE.match(line.strip())
        if not match:
            continue

        key = normalize_field_name(match.group(1))
        value = match.group(2).strip()

        if key == "title" and current:
            citations.append(current)
            current = {}

        current[key] = value

    if current:
        citations.append(current)

    return citations


def build_text(heading: str, body: str, layer: str) -> tuple[str, list[dict[str, str]]]:
    if layer != "evidence":
        return f"{heading}\n\n{body}".strip(), []

    blocks = extract_labeled_blocks(body)
    evidence_summary = clean_lines(blocks.get("Evidence summary", []))
    practical_use = clean_lines(blocks.get("Practical PaceUp use", []))
    citations = parse_citations(blocks.get("Citation", []))

    parts = [heading]
    if evidence_summary:
        parts.append(f"Evidence summary:\n{evidence_summary}")
    if practical_use:
        parts.append(f"Practical PaceUp use:\n{practical_use}")

    return "\n\n".join(parts).strip(), citations


def build_chunks(layer: str, source_path: Path) -> list[dict[str, object]]:
    markdown = source_path.read_text(encoding="utf-8")
    title, sections = split_sections(markdown)
    source_slug = slugify(source_path.stem)
    chunks: list[dict[str, object]] = []

    for index, section in enumerate(sections, start=1):
        text, citations = build_text(section["heading"], section["body"], layer)
        if not text:
            continue

        chunk_id = f"{layer}-{source_slug}-{index:03d}"
        chunk = {
            "id": chunk_id,
            "layer": layer,
            "source": source_path.name,
            "source_path": repo_relative(source_path),
            "document_title": title,
            "heading": section["heading"],
            "text": text,
            "word_count": len(re.findall(r"\b\w+\b", text)),
            "citations": citations,
        }
        chunks.append(chunk)

    return chunks


def build_index(include_readme: bool = False) -> dict[str, object]:
    all_chunks: list[dict[str, object]] = []
    sources: list[dict[str, object]] = []

    for layer, root in SOURCE_DIRS:
        for source_path in markdown_files(root, include_readme=include_readme):
            chunks = build_chunks(layer, source_path)
            if not chunks:
                continue

            all_chunks.extend(chunks)
            sources.append(
                {
                    "layer": layer,
                    "source": source_path.name,
                    "source_path": repo_relative(source_path),
                    "chunk_count": len(chunks),
                }
            )

    return {
        "index_version": 1,
        "description": "PaceUp local RAG source index. Embeddings are added in a later step.",
        "source_dirs": [
            {"layer": layer, "path": repo_relative(path)}
            for layer, path in SOURCE_DIRS
        ],
        "source_count": len(sources),
        "chunk_count": len(all_chunks),
        "sources": sources,
        "chunks": all_chunks,
    }


def write_index(output_path: Path, include_readme: bool = False) -> dict[str, object]:
    index = build_index(include_readme=include_readme)
    if not index["chunks"]:
        raise SystemExit("No RAG chunks were generated.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local JSON RAG index from PaceUp markdown knowledge files."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path. Defaults to data/rag_index.json.",
    )
    parser.add_argument(
        "--include-readme",
        action="store_true",
        help="Include README.md files in the index. Disabled by default.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = args.output
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    index = write_index(output_path, include_readme=args.include_readme)
    print(
        f"Wrote {index['chunk_count']} chunks from {index['source_count']} sources "
        f"to {repo_relative(output_path)}"
    )


if __name__ == "__main__":
    main()

