# PaceUp Knowledge Base

This folder contains trusted coaching guidance for the future PaceUp RAG pipeline.

Write entries as short markdown sections. Each section should stand on its own because the RAG index will split these files into chunks and retrieve only the most relevant pieces for a user question.

## Writing Rules

- Keep guidance practical, specific, and easy to quote.
- Prefer short paragraphs over long essays.
- Put one main idea in each paragraph.
- Avoid advice that requires medical diagnosis.
- For injury, illness, medication, or severe pain questions, recommend a qualified professional.
- Update or remove outdated guidance before rebuilding the RAG index.

## Planned RAG Flow

1. Load markdown files from `data/knowledge`.
2. Split by headings and paragraph length.
3. Embed each chunk.
4. Store chunk text, source file, heading, and embedding.
5. Retrieve the top matching chunks for each chat prompt.
6. Add those chunks to the PaceUp coach prompt.

