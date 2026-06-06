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

PRIVATE ?= ../aprog-private

SLUGS          := $(notdir $(wildcard assignments/*))
ZIPS           := $(patsubst %,dist/%-gradescope.zip,$(SLUGS))
VERIFY_TARGETS := $(patsubst %,verify-%,$(SLUGS))

.PHONY: all venv install dev uninstall check lint format typecheck test \
        test-verbose test-fast test-verbose-fast test-unit test-integration test-system \
        version self-esteem clean zips verify $(VERIFY_TARGETS)

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

# -- zip packaging and verification -------------------------------------------

zips: $(ZIPS)

verify:
ifdef SLUG
	$(VENV)/aprog generate-config $(SLUG) --force
	@scripts/verify-in-tmp.sh $(SLUG) $(abspath $(PRIVATE)) $(CURDIR) $(abspath $(VENV))/aprog
else
	$(MAKE) $(VERIFY_TARGETS)
endif

define SLUG_RULES
dist/$(1)-gradescope.zip: \
    $$(shell find assignments/$(1) -type f 2>/dev/null) \
    $$(shell find $(PRIVATE)/grader/$(1) -type f 2>/dev/null)
	@mkdir -p dist
	$(VENV)/aprog generate-config $(1) --force
	$(VENV)/aprog package-gradescope $(1) --private $(PRIVATE)

verify-$(1):
	@scripts/verify-in-tmp.sh $(1) $(abspath $(PRIVATE)) $(CURDIR) $(abspath $(VENV))/aprog

endef

$(foreach slug,$(SLUGS),$(eval $(call SLUG_RULES,$(slug))))
