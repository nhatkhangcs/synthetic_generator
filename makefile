# Command
PYTHON = python
PIP = pip
VENV_DIR_NAME = .venv
CWD = $(shell pwd)

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S), Linux)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate
else ifeq ($(UNAME_S), Darwin)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate  # macOS
else  # Assume Windows
	ACTIVATE = .\\$(VENV_DIR_NAME)\\Scripts\\activate
endif

# Color
RED = \033[1;91m
GREEN = \033[1;92m
YELLOW = \033[1;93m
RESET = \033[0m

PY_VERSION := $(shell $(ACTIVATE) && $(PYTHON) --version)

.PHONY: help test package clean install venv check_env

help:	### The following lines will print the available commands when entering just 'make'
ifeq ($(UNAME_S), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else ifeq ($(UNAME_S), Windows) # For Window
	@findstr "##" $(MAKEFILE_LIST) | findstr /v "@findstr" | sort
else # For MaxOS
	@awk -F ':.*###' '$$0 ~ FS {printf "\033[36m%15s\033[0m%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

check_env:	### Checking environment, e.g. script creating venv && operating system && ...
	@echo "CWD    :$(GREEN) $(CWD)				$(RESET)"
	@echo "MAKE   :$(GREEN)$(MAKEFILE_LIST)		$(RESET)"
	@echo "OS     :$(GREEN) $(UNAME_S)			$(RESET)"
	@echo "VENV   :$(GREEN) $(ACTIVATE)			$(RESET)"
	@echo "PY_VER :$(GREEN) $(PY_VERSION)		$(RESET)"

venv:	### Create virtual environment
	@echo "$(GREEN)Creating virtual environment$(RESET)"
	$(ACTIVATE) && $(PYTHON) -m venv $(VENV_DIR_NAME)

test: venv ### Runs all the project tests
	@echo "$(GREEN)Run tests$(RESET)"
	$(ACTIVATE) && $(PIP) install pytest && $(PYTHON) -m pytest tests/

package: clean ### Runs the project setup
	@echo "$(version)" > VERSION
	$(ACTIVATE) && $(PYTHON) -m build --wheel
	$(ACTIVATE) && $(PYTHON) -m twine check dist/*

clean: ### Removes build binaries file and distribute file
	@echo "$(RED)Removing build and dist directories $(RESET)"
	rm -rf build dist

install_dev: venv install ### Installs required dependencies for developers
	@echo "$(GREEN)Installing requirements for $(YELLOW)developers $(RESET)"
	$(ACTIVATE) && $(PIP) install -r requirements/requirements-dev.txt
	$(ACTIVATE) && $(PIP) install -e ".[dev,test]"

install: venv ### Installs required dependencies for users
	@echo "$(GREEN)Installing requirements for $(YELLOW)users $(RESET)"
	$(ACTIVATE) && $(PIP) install -r requirements/requirements.txt
	$(ACTIVATE) && $(PIP) install -e .
