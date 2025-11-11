from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class Source(BaseModel):
    nct_id: str
    tag: Literal["title", "summary", "eligibility", "condition", "other"] = "other"
    snippet: str


class AskMeta(BaseModel):
    latency_ms: int
    retrieved_k: int
    model: str


class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    meta: AskMeta


class MetaResponse(BaseModel):
    embed_model: str
    llm_model: str
    index_size: int

