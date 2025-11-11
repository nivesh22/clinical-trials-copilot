Clinical Trials Copilot — RAG over ClinicalTrials.gov
====================================================

What & Why
----------
- Privacy-first assistant to query public clinical trial data with citations.
- Portfolio-credible stack that runs locally or on free tiers.

Architecture
------------
Monorepo contains:
- FastAPI backend with `/ask`, `/ask/stream`, `/meta`, `/healthz`.
- Next.js (App Router) UI with an internal proxy route `/api/ask`.
- Airflow DAG for daily ingest (stubbed), Docker/Compose, K8s manifests, Jenkins.

Quickstart (Local)
------------------
1) Backend
- `python -m venv .venv && . .venv/bin/activate`
- `pip install -r requirements.txt`
- `make api` (serves on http://localhost:8000)

2) UI
- `cd ui && npm i`
- `npm run dev` (http://localhost:3000)

Compose
-------
- `make compose-up`
- Open http://localhost:3000 and http://localhost:8000/healthz
- `make compose-down` to stop

Kubernetes (optional, kustomize)
--------------------------------
- `kubectl create ns trials`
- `kubectl apply -k k8s/`
- `kubectl -n trials port-forward svc/ctc-ui 3000:3000 &`
- `kubectl -n trials port-forward svc/ctc-api 8000:8000 &`

API Contract
------------
- POST `/ask` → `{ answer, sources, meta }`
- POST `/ask/stream` → SSE `token` events and final `done` with payload
- GET `/meta` → `{ embed_model, llm_model, index_size }`
- GET `/healthz` → `ok`

How to change the model
-----------------------
- Edit `.env` or set `LLM_MODEL`/`EMBED_MODEL` envs. When using Compose, pass via environment or `.env` file.

How to re-index
---------------
- Implement `app/rag/ingest.py` to load → embed → persist FAISS under `var/index`.
- Airflow DAG `airflow/dags/clinical_trials_ingest.py` calls the ingest (stubbed).

Frontend notes
--------------
- Proxy route at `ui/app/api/ask/route.ts` forwards to FastAPI using `process.env.API_BASE` (server-only).
- `/chat` calls the proxy; `/status` calls `/meta` for index/model info.

CI/CD
-----
- GitHub Actions workflow at `.github/workflows/ci.yml` runs lint/tests for backend and frontend, builds Docker images, and does a compose-based smoke test.

License
-------
MIT. Use public trial data only; no PHI/PII.
