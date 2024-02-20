RYE_EXEC ?= rye run
PYTHON_VERSION ?= 3.12
PATH := $(HOME)/.rye/shims:$(PATH)

SHELL := /bin/bash

PYTHON_FILES := $(shell find src/ -name '*.py')
RST_FILES := $(shell find docs/ -name '*.rst' -o -name 'conf.py')
THEME_FILES := $(shell find docs/source/_static -type f)

PYTEST_PATHS ?= "src/"
HYPOTHESIS_PROFILE ?= dev
PYTEST_HYPOTHESIS_ARGS ?=
PYTEST_EXTRA_ARGS ?=
PYTEST_FAILURE_ARGS ?= --ff --maxfail 1
PYTEST_ARGS ?= -vv $(PYTEST_FAILURE_ARGS) $(PYTEST_EXTRA_ARGS) $(PYTEST_HYPOTHESIS_ARGS)

install:
	rye self update || curl -sSf https://rye-up.com/get | bash
	rye pin --relaxed $(PYTHON_VERSION)
	rye sync
	cp -f requirements-dev.lock requirements-dev-py$$(echo $(PYTHON_VERSION) | sed "s/\.//").lock
.PHONY: install


test: $(PYTHON_FILES)
	@rm -f .coverage*
	@if [ -z "$(PYTEST_WORKERS)" ]; then \
        $(RYE_EXEC) pytest --cov-report= --cov-config=pyproject.toml --cov=src/ $(PYTEST_ARGS) $(PYTEST_PATHS); \
    else \
        $(RYE_EXEC) pytest --cov-report= --cov-config=pyproject.toml --cov=src/ -n $(PYTEST_WORKERS) $(PYTEST_ARGS) $(PYTEST_PATHS); \
    fi
.PHONY: test


docs/build: $(PYTHON_FILES) $(RST_FILES) $(THEME_FILES)
	@bash -c 'source .venv/bin/activate; make -C docs html'
	@touch docs/build

CADDY_SERVER_PORT ?= 9999
caddy: docs/build
	@docker run --rm -p $(CADDY_SERVER_PORT):$(CADDY_SERVER_PORT) \
         -v $(PWD)/docs/build/html:/var/www -it caddy \
         caddy file-server --browse --listen :$(CADDY_SERVER_PORT) --root /var/www
.PHONY: caddy

mypy:
	@$(RYE_EXEC) tox -e system-staticcheck
.PHONY: mypy

format:
	@$(RYE_EXEC) ruff --fix src/
	@$(RYE_EXEC) isort src/
	@$(RYE_EXEC) ruff format src/
.PHONY: format

lint:
	@$(RYE_EXEC) ruff src/
	@$(RYE_EXEC) ruff format --check src/
	@$(RYE_EXEC) isort --check src/
.PHONY: lint


shell:
	@$(RYE_EXEC) ipython
.PHONY: shell
