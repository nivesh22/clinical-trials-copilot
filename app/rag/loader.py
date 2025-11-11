from __future__ import annotations

from typing import Dict, Iterable, List, Optional

import requests

from app.config import settings


Fields = List[str]


DEFAULT_FIELDS: Fields = [
    # IDs
    "nctId",
    # Modules (v2 nested paths)
    "protocolSection.identificationModule.officialTitle",
    "conditionsModule.conditions",
    "descriptionModule.briefSummary",
    "eligibilityModule.eligibilityCriteria",
]


def _join_fields(fields: Fields) -> str:
    return ",".join(fields)


def fetch_trials(
    query: Optional[str] = None,
    *,
    fields: Fields = DEFAULT_FIELDS,
    page_size: int | None = None,
    max_records: int = 500,
    extra_params: Optional[Dict[str, str]] = None,
) -> List[dict]:
    """Fetch trial records from ClinicalTrials.gov API v2 with pagination.

    This function does not require network at test time; unit tests should mock requests.get.

    Args:
        query: Optional free-text query (applied as API filter if provided).
        fields: List of field paths to request from the API.
        page_size: Page size (defaults to CTGOV_PAGE_SIZE env).
        max_records: Upper bound on number of records to return.
        extra_params: Additional query params passed through (e.g., studyType, status, etc.).

    Returns:
        A list of dicts (raw flattened-ish study entries) limited to max_records.
    """

    base = settings.ctgov_api_base.rstrip("/")
    url = f"{base}/studies"
    size = page_size or settings.ctgov_page_size
    params: Dict[str, str] = {
        "pageSize": str(size),
        "fields": _join_fields(fields),
    }

    # Attempt common v2 query param; allow override via extra_params.
    # Some deployments support `query.term`; others rely on different filters.
    if query:
        params["query.term"] = query

    if extra_params:
        params.update(extra_params)

    all_items: List[dict] = []
    page_token: Optional[str] = None

    while len(all_items) < max_records:
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get(url, params=params, timeout=settings.ctgov_timeout_s)
        resp.raise_for_status()
        data = resp.json()

        studies = data.get("studies") or data.get("results") or []
        for st in studies:
            all_items.append(_flatten_study(st))
            if len(all_items) >= max_records:
                break

        # Pagination token keys vary; handle common cases
        page_token = data.get("nextPageToken") or data.get("next_page_token")
        if not page_token or not studies:
            break

    return all_items


def _flatten_study(study: dict) -> dict:
    """Extract and normalize fields used by our RAG pipeline.

    The v2 response nests values under protocolSection.* modules. Be defensive: use get chains.
    """

    def g(d: dict, path: str, default: Optional[str] = None):
        cur: object = d
        for key in path.split("."):
            if not isinstance(cur, dict):
                return default
            cur = cur.get(key)
            if cur is None:
                return default
        return cur

    nct_id = g(study, "nctId", "")
    title = g(study, "protocolSection.identificationModule.officialTitle", "")
    conditions = g(study, "conditionsModule.conditions", []) or []
    brief = g(study, "descriptionModule.briefSummary", "")
    elig = g(study, "eligibilityModule.eligibilityCriteria", "")

    return {
        "nct_id": nct_id,
        "officialTitle": title,
        "conditions": conditions,
        "briefSummary": brief,
        "eligibilityCriteria": elig,
    }


def chunk_documents(docs: Iterable[dict], max_tokens: int = 700) -> List[dict]:
    """Simple word-based chunking for long fields; returns chunk docs with metadata.

    This is an approximation (word-based) standing in for tokenization.
    """
    chunks: List[dict] = []
    for d in docs:
        nct = d.get("nct_id", "")
        # Build tagged text pieces
        pieces = [
            ("title", d.get("officialTitle") or ""),
            ("summary", d.get("briefSummary") or ""),
            ("eligibility", d.get("eligibilityCriteria") or ""),
        ]
        for tag, text in pieces:
            words = text.split()
            if not words:
                continue
            for i in range(0, len(words), max_tokens):
                chunk_text = " ".join(words[i : i + max_tokens])
                chunks.append({
                    "nct_id": nct,
                    "tag": tag,
                    "text": chunk_text,
                })
    return chunks


def load_and_chunk(
    query: Optional[str] = None,
    *,
    max_records: int = 500,
    fields: Fields = DEFAULT_FIELDS,
    page_size: int | None = None,
    extra_params: Optional[Dict[str, str]] = None,
    max_tokens: int = 700,
) -> List[dict]:
    """High-level convenience: fetch trials and produce chunk docs for embedding.

    Returns a list of dicts: {nct_id, tag, text} ready for embedding and FAISS upsert.
    """
    docs = fetch_trials(
        query=query,
        fields=fields,
        page_size=page_size,
        max_records=max_records,
        extra_params=extra_params,
    )
    return chunk_documents(docs, max_tokens=max_tokens)
