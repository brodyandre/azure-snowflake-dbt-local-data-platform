PYTHON ?= python3

.PHONY: up down logs ps clean install lint format test check batch

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
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

test:
	$(PYTHON) -m pytest

check: lint test

batch:
	$(PYTHON) -m src.batch.run_batch_pipeline
