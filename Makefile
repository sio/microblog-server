include Makefile.venv
include makefiles/*.mk


.PHONY: test
test: | $(VENV)/tox $(CODECOLOR)
	$(VENV)/tox
