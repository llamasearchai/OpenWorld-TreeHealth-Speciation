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
