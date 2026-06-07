.PHONY: up down logs ps clean install lint format test check

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down -v

install:
	python -m pip install -r requirements.txt

lint:
	python -m ruff check .

format:
	python -m ruff format .

test:
	python -m pytest

check: lint test
