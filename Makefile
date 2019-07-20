# Makefile for Sphinx documentation

.PHONY: help
help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  docs       to build the docs"

.PHONY: tests
tests:
	pytest tests

.PHONY: docs
docs:
	rm -rf docs/html*
	sphinx-apidoc -f -e -o docs/src ndna
	sphinx-build -b html docs/src docs/html
