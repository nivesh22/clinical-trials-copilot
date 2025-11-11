from __future__ import annotations

import json
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.config import settings
from app.models.io import AskRequest, AskResponse, MetaResponse
from app.rag.chain import answer, stream_tokens
from app.rag.utils import index_size

app = FastAPI(title="Clinical Trials Copilot API", version="0.1.0")


@app.get("/healthz", response_class=PlainTextResponse)
async def healthz() -> str:
    return "ok"


@app.get("/meta", response_model=MetaResponse)
async def meta() -> MetaResponse:
    return MetaResponse(
        embed_model=settings.embed_model,
        llm_model=settings.llm_model,
        index_size=index_size(settings.index_dir),
    )


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    if not req.question.strip():
        raise HTTPException(status_code=422, detail="question must not be empty")
    return answer(req.question)


@app.post("/ask/stream")
async def ask_stream(req: AskRequest):
    async def event_gen() -> AsyncGenerator[bytes, None]:
        # Use the stub synchronous generator and adapt to async
        for evt in stream_tokens(req.question):
            if evt["type"] == "token":
                payload = f"event: token\ndata: {evt['data']}\n\n"
            else:
                payload = "event: done\n" + "data: " + json.dumps(evt["data"]) + "\n\n"
            yield payload.encode("utf-8")

    return StreamingResponse(event_gen(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.api_port, reload=True)
