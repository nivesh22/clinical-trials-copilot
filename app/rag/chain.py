from __future__ import annotations

import time
from typing import List

from app.config import settings
from app.models.io import AskMeta, AskResponse, Source
from app.rag.retriever import retrieve


def answer(question: str, retrieved_k: int = 3) -> AskResponse:
    """Synthesize an answer from retrieved documents (stubbed).

    In production, assemble a proper prompt and call the LLM via Ollama,
    using retrieved context. Here we simulate latency and return a simple answer.
    """

    t0 = time.perf_counter()
    hits = retrieve(question, k=retrieved_k)
    # Simple answer synthesis (placeholder)
    ans = (
        "Here is a summary based on available clinical trial records. "
        "Consult the listed NCT sources for details."
    )
    sources: List[Source] = [
        Source(nct_id=h[0], tag=h[1], snippet=h[2]) for h in hits
    ]
    latency_ms = int((time.perf_counter() - t0) * 1000)
    meta = AskMeta(latency_ms=latency_ms, retrieved_k=len(sources), model=settings.llm_model)
    return AskResponse(answer=ans, sources=sources, meta=meta)


def stream_tokens(question: str, retrieved_k: int = 3):
    """Generator yielding token-like chunks and a final done event payload.

    Yields dicts with either {type: 'token', data: '...'} or
    {type: 'done', data: {answer, sources, meta}}.
    """
    resp = answer(question, retrieved_k=retrieved_k)
    # Naive tokenization by words
    for word in resp.answer.split(" "):
        yield {"type": "token", "data": word + " "}
        time.sleep(0.02)
    yield {"type": "done", "data": resp.model_dump()}
