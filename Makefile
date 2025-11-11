.PHONY: api ui dev compose-up compose-down test lint

api:
	uvicorn app.main:app --reload --port $${API_PORT:-8000}

ui:
	cd ui && npm run dev

compose-up:
	docker compose -f docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f docker/docker-compose.yml down -v

test:
	pytest --junitxml=test-results/py-tests.xml

lint:
	ruff check

