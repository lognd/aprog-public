UV     := uv
PYTEST := $(UV) run pytest
RUFF   := $(UV) run ruff
TY     := $(UV) run ty
APROG  := .venv/bin/aprog

PRIVATE ?= ../aprog-private

SLUGS          := $(notdir $(wildcard assignments/*))
ZIPS           := $(patsubst %,dist/%-gradescope.zip,$(SLUGS))
VERIFY_TARGETS := $(patsubst %,verify-%,$(SLUGS))

.PHONY: all install dev check lint format typecheck test \
        test-verbose test-fast test-verbose-fast test-unit test-integration test-system \
        version self-esteem clean zips verify hashes $(VERIFY_TARGETS)

all: dev check test

install:
	@$(UV) sync --no-group dev

dev:
	@$(UV) sync

check: format lint typecheck

lint:
	@$(RUFF) check src/ tests/

format:
	@$(RUFF) format src/ tests/
	@$(RUFF) check --fix src/ tests/

typecheck:
	@$(TY) check src/

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
	@$(UV) --version
	@$(PYTEST) --version
	@$(RUFF) --version
	@$(TY) --version

self-esteem:
	@cloc --vcs=git src/

clean:
	rm -rf .venv dist/ build/ *.egg-info src/*.egg-info \
	       __pycache__ .mypy_cache .ruff_cache .pytest_cache

# -- zip packaging and verification -------------------------------------------

zips: $(ZIPS)

hashes:
	find . -type d \( -name ".claude" -o -name ".git" -o -name ".idea" -o -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".venv" \) -prune -o -type f -exec dos2unix {} +
	$(APROG) generate-config --all --force

verify:
ifdef SLUG
	@scripts/verify-in-tmp.sh $(SLUG) $(abspath $(PRIVATE)) $(CURDIR) $(abspath $(APROG))
else
	$(APROG) verify --all --public $(CURDIR) --private $(abspath $(PRIVATE))
endif

define SLUG_RULES
dist/$(1)-gradescope.zip: \
    $$(shell find assignments/$(1) -type f 2>/dev/null) \
    $$(shell find $(PRIVATE)/grader/$(1) -type f 2>/dev/null)
	@mkdir -p dist
	$(APROG) generate-config $(1) --force
	$(APROG) package-gradescope $(1) --private $(PRIVATE)

verify-$(1):
	@scripts/verify-in-tmp.sh $(1) $(abspath $(PRIVATE)) $(CURDIR) $(abspath $(APROG))

endef

$(foreach slug,$(SLUGS),$(eval $(call SLUG_RULES,$(slug))))

# Overlay a local editable lograder for hacking on both repos at once.
dev-local: dev
	@$(UV) pip install -e "$(LOGRADER)"
