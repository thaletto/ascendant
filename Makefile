.DEFAULT_GOAL := help

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PYRIGHT := $(VENV)/bin/pyright
PYCODESTYLE := $(VENV)/bin/pycodestyle

.PHONY: help test typecheck lint check

help: ## Show available development commands.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## Run the pytest suite.
	$(PYTHON) -m pytest -q

typecheck: ## Run Pyright for the library and tests.
	mkdir -p build/pyright
	ln -sfn ../../src build/pyright/ascendant
	$(PYRIGHT) src tests --warnings

lint: ## Run PEP 8 checks for the library and test suite.
	$(PYCODESTYLE) src tests

check: test typecheck lint ## Run all verification checks.
