from __future__ import annotations

from typing import List, Tuple


def retrieve(question: str, k: int = 3) -> List[Tuple[str, str, str]]:
    """Stub retriever. Returns a few placeholder (nct_id, tag, snippet) tuples.

    Replace with FAISS-backed retrieval. Keep signature stable.
    """

    placeholders = [
        ("NCT01234567", "eligibility", "Adults 18-65 with confirmed diagnosis."),
        ("NCT07654321", "summary", "Phase II randomized trial of treatment X."),
        ("NCT00999999", "title", "A Study of Y in Condition Z."),
    ]
    return placeholders[:k]

