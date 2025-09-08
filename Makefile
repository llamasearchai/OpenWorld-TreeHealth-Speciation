PY=python3
PIP=pip
UVICORN=uvicorn
APP=openworld_treehealth.app:app

.PHONY: install dev test run lint format docker-build docker-run

install:
	$(PY) -m venv .venv && . .venv/bin/activate && \
	python -m pip install -U pip && \
	pip install -e .

dev:
	$(PY) -m venv .venv && . .venv/bin/activate && \
	python -m pip install -U pip && \
	pip install -e ".[dev]"

test:
	. .venv/bin/activate && pytest -q

run:
	. .venv/bin/activate && $(UVICORN) $(APP) --host 0.0.0.0 --port 8000 --reload

lint:
	. .venv/bin/activate && ruff check .

format:
	. .venv/bin/activate && ruff format .

docker-build:
	docker build -t openworld-treehealth:latest .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env openworld-treehealth:latest

.PHONY: setup test lint fmt type audit precommit docs docs-serve dashboard train build docker clean

setup:
	python -m pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check openworld_tshm tests

fmt:
	ruff check --fix openworld_tshm tests

type:
	mypy openworld_tshm

audit:
	pip-audit || true

docs:
	mkdocs build --strict

dashboard:
	openworld-tshm dashboard --reload

train:
	openworld-tshm train --seed 42 --out-dir artifacts/run_$$RANDOM

build:
	hatch build

docker:
	docker build -t openworld-tshm .

precommit:
	pre-commit install && pre-commit run --all-files || true

docs-serve:
	mkdocs serve -a 127.0.0.1:8001

tag:
	@if [ -z "$(VERSION)" ]; then echo "VERSION not set (e.g., make tag VERSION=0.2.1)"; exit 1; fi
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	echo "Created tag v$(VERSION). Push with: git push origin v$(VERSION)"

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache site build dist provenance/ledger.jsonl
	rm -rf artifacts outputs temp .tmp
