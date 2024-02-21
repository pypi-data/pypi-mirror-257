# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

VENV ?= venv

BASE_DIR = $(shell pwd)

.PHONY: all
all: setup

$(VENV):
	uv venv $(VENV)

.PHONY: setup
setup: | $(VENV)
	uv pip install -e .

.PHONY: clean
clean:
	rm -rf node_modules/ $(VENV)
	find -name __pycache__ -type d -exec rm -rf '{}' \;
	find -name \*.pyc -type f -exec rm -f '{}' \;
