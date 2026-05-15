# PaceUp Evidence Layer

This folder contains study-backed evidence summaries for the PaceUp RAG pipeline.

Each entry should be short enough to retrieve as a standalone chunk. Use this layer to support claims with research, guidelines, systematic reviews, meta-analyses, and position stands. Do not paste full papers or abstracts into these files.

## Entry Format

Each section should include:

- Evidence summary
- Practical PaceUp use
- Citation metadata

## Source Rules

- Prefer systematic reviews, meta-analyses, consensus statements, and position stands.
- Use primary source pages such as DOI landing pages, journal pages, PMC, guideline pages, or PubMed when a better primary landing page is not available.
- Avoid defaulting every citation URL to PubMed if the DOI or journal landing page is available.
- Include source title, authors, year, source type, DOI when available, and URL.
- Paraphrase findings. Do not copy long passages from papers.
- If evidence is mixed or low quality, say so clearly.

## Planned RAG Use

The coaching layer in `data/knowledge` defines PaceUp's voice and practical policy. This evidence layer gives the model credible support for specific claims.

When both layers are retrieved, the answer should combine practical coaching with evidence-aware caution.
