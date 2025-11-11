from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.text == "ok"


def test_meta():
    r = client.get("/meta")
    assert r.status_code == 200
    body = r.json()
    assert "embed_model" in body and "llm_model" in body and "index_size" in body


def test_ask():
    r = client.post("/ask", json={"question": "What are common eligibility criteria?"})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body.get("answer"), str)
    assert len(body.get("sources", [])) >= 1
    assert body.get("meta", {}).get("retrieved_k") >= 1
