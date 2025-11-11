from __future__ import annotations

from pathlib import Path
from typing import List

from app.rag.loader import load_and_chunk


def run_ingest(index_dir: str, query: str | None = None, max_records: int = 500) -> List[dict]:
    """Placeholder ingest: loads and chunks data and returns chunk docs.

    Replace return with actual embedding + FAISS persistence into index_dir.
    """
    Path(index_dir).mkdir(parents=True, exist_ok=True)
    chunks = load_and_chunk(query=query, max_records=max_records)
    # TODO: embed and persist. For now, return chunks for inspection.
    return chunks
