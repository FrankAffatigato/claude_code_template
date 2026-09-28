.PHONY: backend frontend test lint seed

backend:
	uvicorn backend.main:app --reload

frontend:
	cd frontend && npm run dev

test:
	pytest -q

lint:
	ruff check backend
	cd frontend && npm run lint

seed:
	python -m backend.scripts.seed
