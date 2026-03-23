SHELL := /bin/bash

.PHONY: setup new-project onboard-project prepare-project-repo check handoff-project

setup:
	bash scripts/setup-workspace.sh

new-project:
	@if [[ -z "$(NAME)" ]]; then \
		echo 'Usage: make new-project NAME="Project Name" GOAL="Initial goal"'; \
		exit 1; \
	fi
	python3 scripts/new-project.py "$(NAME)" "$(or $(GOAL),Define initial project goal.)"

onboard-project:
	@if [[ -z "$(SLUG)" ]]; then \
		echo 'Usage: make onboard-project SLUG="project-slug" NAME="Optional Project Name" GOAL="Initial goal"'; \
		exit 1; \
	fi
	python3 scripts/onboard-project.py "$(SLUG)" $(if $(NAME),--name "$(NAME)") --goal "$(or $(GOAL),Document the initial project goal.)"

prepare-project-repo:
	@if [[ -z "$(SLUG)" ]]; then \
		echo 'Usage: make prepare-project-repo SLUG="project-slug" NAME="Optional Project Name" LICENSE="Apache-2.0|MIT|none"'; \
		exit 1; \
	fi
	python3 scripts/prepare-project-repo.py "$(SLUG)" $(if $(NAME),--name "$(NAME)") --license "$(or $(LICENSE),Apache-2.0)" $(if $(NO_CI),--no-ci)

check:
	bash -n scripts/setup-workspace.sh
	bash -n scripts/new-project.sh
	python3 -m py_compile scripts/new-project.py
	python3 -m py_compile scripts/onboard-project.py
	python3 -m py_compile scripts/prepare-project-repo.py
	python3 -m py_compile scripts/project_scaffold.py
	python3 -m py_compile scripts/clone-project.py
	python3 -m py_compile scripts/handoff-project.py

handoff-project:
	@if [[ -z "$(SLUG)" ]]; then \
		echo 'Usage: make handoff-project SLUG="project-slug"'; \
		exit 1; \
	fi
	python3 scripts/handoff-project.py "$(SLUG)"
