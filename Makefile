.DEFAULT_GOAL := help

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PYRIGHT := $(VENV)/bin/pyright
BASEDPYRIGHT := $(VENV)/bin/basedpyright
PYCODESTYLE := $(VENV)/bin/pycodestyle

.PHONY: help test typecheck typecheck-mcp lint check

help: ## Show available development commands.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## Run the pytest suite.
	$(PYTHON) -m pytest -q

typecheck: ## Run Pyright for the library and tests.
	$(PYRIGHT) ascendant mcp/src tests --warnings

typecheck-mcp: ## Run strict Basedpyright for the hosted MCP package.
	cd mcp && ../$(BASEDPYRIGHT) --project pyproject.toml

lint: ## Run PEP 8 checks for the library and test suite.
	$(PYCODESTYLE) ascendant tests

check: test typecheck typecheck-mcp lint ## Run all verification checks.
