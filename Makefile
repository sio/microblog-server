SETUP_PY=setup.cfg
include Makefile.venv
include makefiles/*.mk

dist: src pyproject.toml setup.cfg Makefile makefiles

.PHONY: run
run: | venv
	$(VENV)/microblog

.PHONY: test
test: | $(VENV)/tox
	$(VENV)/tox

.PHONY: test-interactive
test-interactive: | $(VENV)/pytest
	$(VENV)/pytest -rA --color=yes -vv --pdb

.PHONY: clean
clean:
	git clean -idx
