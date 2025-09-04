.PHONY: setup test lint fmt dashboard train build docker

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

dashboard:
	openworld-tshm dashboard --reload

train:
	openworld-tshm train --seed 42 --out-dir artifacts/run_$$RANDOM

build:
	hatch build

docker:
	docker build -t openworld-tshm .

