VENV := .venv/bin
VENV_PY := $(VENV)/python

ifeq ($(wildcard $(VENV_PY)),)
PYTHON := python3
PIP    := pip3
BLACK  := black
RUFF   := ruff
MYPY   := mypy
ISORT  := isort
PYTEST := pytest
else
PYTHON := $(VENV_PY)
PIP    := $(VENV)/pip3
BLACK  := $(VENV)/black
RUFF   := $(VENV)/ruff
MYPY   := $(VENV)/mypy
ISORT  := $(VENV)/isort
PYTEST := $(VENV)/pytest
endif

LOGRADER ?= ../lograder

.PHONY: all venv install dev uninstall check lint format typecheck test \
        test-verbose test-fast test-verbose-fast test-unit test-integration test-system \
        version self-esteem clean

all: uninstall dev check test

venv:
	python3 -m venv .venv

uninstall:
	@$(PIP) uninstall -y aprog 2>/dev/null || true

install: venv
	@$(PIP) install -e "$(LOGRADER)" -e .

dev: venv
	@$(PIP) install -e "$(LOGRADER)" -e ".[dev]"

check:
	@$(BLACK) src/ tests/
	@$(RUFF) format src/ tests/
	@$(ISORT) src/ tests/
	@$(MYPY) --config-file mypy.ini src/ tests/

lint:
	@$(RUFF) check src/ tests/

format:
	@$(BLACK) src/ tests/
	@$(ISORT) src/ tests/

typecheck:
	@$(MYPY) --config-file mypy.ini src/ tests/

test:
	@$(PYTEST)

test-all:
	@$(PYTEST) --no-testmon

test-verbose:
	@$(PYTEST) -v -s

test-fast:
	@$(PYTEST) -m "not slow"

test-verbose-fast:
	@$(PYTEST) -v -s -m "not slow"

test-unit:
	@$(PYTEST) tests/unit/ -v --no-testmon

test-integration:
	@$(PYTEST) tests/integration/ -v --no-testmon

test-system:
	@$(PYTEST) tests/system/ -v -s -m "slow" --no-testmon

version:
	@$(PYTHON) --version
	@$(PIP) --version
	@$(PYTEST) --version
	@$(BLACK) --version
	@$(RUFF) --version
	@$(ISORT) --version
	@$(MYPY) --version

self-esteem:
	@cloc --vcs=git src/

clean:
	rm -rf .venv dist/ build/ *.egg-info src/*.egg-info \
	       __pycache__ .mypy_cache .ruff_cache .pytest_cache
