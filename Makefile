PYTHON = .venv/bin/python
RUFF   = .venv/bin/ruff
PYTEST = .venv/bin/pytest

.PHONY: install lint test run

install:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"

lint:
	$(RUFF) format .
	$(RUFF) check .

test:
	$(PYTEST) tests -vvv

run:
	$(PYTHON) main.py
