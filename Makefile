VENV_PYTHON := .venv/bin/python
PYTHON ?= python3

ifneq ($(origin PYTHON), command line)
ifneq ($(wildcard $(VENV_PYTHON)),)
PYTHON := $(VENV_PYTHON)
endif
endif

.PHONY: up down logs ps clean install lint format test check batch streaming-producer streaming-consumer streaming-demo

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

streaming-producer:
	$(PYTHON) -m src.streaming.producer_events

streaming-consumer:
	$(PYTHON) -m src.streaming.consumer_events --max-events 20

streaming-demo:
	$(PYTHON) -m src.streaming.producer_events
	$(PYTHON) -m src.streaming.consumer_events --max-events 20
