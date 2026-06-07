.PHONY: install lint format test check

install:
	python -m pip install -r requirements.txt

lint:
	python -m ruff check .

format:
	python -m ruff format .

test:
	python -m pytest

check: lint test
