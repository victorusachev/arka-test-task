run:
	poetry run uvicorn backend.main:create_app --reload --app-dir src

fmt:
	ruff check -s --fix --exit-zero src

lint list_strict:
	mypy src
	ruff check src

lint_fix: fmt lint

migrate:
	poetry run python -m yoyo apply -vvv --batch --database "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_NAME}" ./src/migrations
