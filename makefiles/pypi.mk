.PHONY: package build
package build: dist
dist: | venv $(VENV)/build
	-$(RM) -rv dist
	$(VENV)/python -m build


.PHONY: upload
upload: dist | $(VENV)/twine
	ls dist/*
	$(VENV)/twine upload --repository testpypi $(TWINE_ARGS) dist/*
	$(VENV)/twine upload $(TWINE_ARGS) dist/*
