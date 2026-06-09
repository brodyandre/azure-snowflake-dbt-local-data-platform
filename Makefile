VENV_PYTHON := .venv/bin/python
VENV_DBT := .venv/bin/dbt
PYTHON ?= python3
DBT_CMD ?= dbt

ifneq ($(origin PYTHON), command line)
ifneq ($(wildcard $(VENV_PYTHON)),)
PYTHON := $(VENV_PYTHON)
endif
endif

ifneq ($(wildcard $(VENV_DBT)),)
DBT_CMD := ../$(VENV_DBT)
endif

.PHONY: up down logs ps clean install lint format test check batch streaming-producer streaming-consumer streaming-demo dbt-debug dbt-run dbt-test dbt-build quality-report validate

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
	$(PYTHON) -m pytest -v

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

dbt-debug:
	cd dbt && DBT_PROFILES_DIR=. $(DBT_CMD) debug --profiles-dir .

dbt-run:
	cd dbt && DBT_PROFILES_DIR=. $(DBT_CMD) run --profiles-dir .

dbt-test:
	cd dbt && DBT_PROFILES_DIR=. $(DBT_CMD) test --profiles-dir .

dbt-build:
	cd dbt && DBT_PROFILES_DIR=. $(DBT_CMD) build --profiles-dir .

quality-report:
	$(PYTHON) -m src.quality.data_quality_report

validate:
	$(PYTHON) -m compileall src dashboard
	$(MAKE) batch
	$(MAKE) streaming-demo
	$(MAKE) dbt-build
	$(MAKE) test
	$(MAKE) quality-report
