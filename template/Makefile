SHELL := /bin/bash

.PHONY: setup new-project check handoff-project

setup:
	bash scripts/setup-workspace.sh

new-project:
	@if [[ -z "$(NAME)" ]]; then \
		echo 'Usage: make new-project NAME="Project Name" GOAL="Initial goal"'; \
		exit 1; \
	fi
	python3 scripts/new-project.py "$(NAME)" "$(or $(GOAL),Define initial project goal.)"

check:
	bash -n scripts/setup-workspace.sh
	bash -n scripts/new-project.sh
	python3 -m py_compile scripts/new-project.py
	python3 -m py_compile scripts/clone-project.py
	python3 -m py_compile scripts/handoff-project.py

handoff-project:
	@if [[ -z "$(SLUG)" ]]; then \
		echo 'Usage: make handoff-project SLUG="project-slug"'; \
		exit 1; \
	fi
	python3 scripts/handoff-project.py "$(SLUG)"
