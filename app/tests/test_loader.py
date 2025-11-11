from __future__ import annotations

from typing import Any

from app.rag.loader import fetch_trials, load_and_chunk


class DummyResp:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self) -> Any:
        return self._payload


def test_fetch_trials_pagination(monkeypatch):
    pages = [
        {
            "studies": [
                {
                    "nctId": "NCT001",
                    "protocolSection": {
                        "identificationModule": {"officialTitle": "T1"}
                    },
                    "conditionsModule": {"conditions": ["A"]},
                    "descriptionModule": {"briefSummary": "S1"},
                    "eligibilityModule": {"eligibilityCriteria": "E1"},
                }
            ],
            "nextPageToken": "abc",
        },
        {
            "studies": [
                {
                    "nctId": "NCT002",
                    "protocolSection": {
                        "identificationModule": {"officialTitle": "T2"}
                    },
                    "conditionsModule": {"conditions": ["B"]},
                    "descriptionModule": {"briefSummary": "S2"},
                    "eligibilityModule": {"eligibilityCriteria": "E2"},
                }
            ],
        },
    ]
    calls = {"i": 0}

    def fake_get(url, params=None, timeout=None):  # type: ignore
        i = calls["i"]
        calls["i"] += 1
        return DummyResp(pages[i])

    import requests

    monkeypatch.setattr(requests, "get", fake_get)
    docs = fetch_trials(query="asthma", max_records=10)
    assert len(docs) == 2
    assert docs[0]["nct_id"] == "NCT001"
    assert docs[1]["nct_id"] == "NCT002"


def test_load_and_chunk(monkeypatch):
    payload = {
        "studies": [
            {
                "nctId": "NCT010",
                "protocolSection": {
                    "identificationModule": {"officialTitle": "Title"}
                },
                "conditionsModule": {"conditions": ["C1"]},
                "descriptionModule": {"briefSummary": "one two three four five"},
                "eligibilityModule": {"eligibilityCriteria": "alpha beta gamma"},
            }
        ]
    }

    def fake_get(url, params=None, timeout=None):  # type: ignore
        return DummyResp(payload)

    import requests

    monkeypatch.setattr(requests, "get", fake_get)

    chunks = load_and_chunk(query="sample", max_records=1, max_tokens=2)
    # Expect multiple chunks due to small max_tokens
    assert len(chunks) >= 2
    assert all("nct_id" in c and "tag" in c and "text" in c for c in chunks)
