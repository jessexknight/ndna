# Makefile for Sphinx documentation

.PHONY: help
help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  tests      to run all tests and coverage"
	@echo "  debug      to run just tests and print output"
	@echo "  cov        to run just coverage report"
	@echo "  docs       to build the docs"

.PHONY: tests
tests:
	bash ci/pylint/get-badge.sh
	pytest --cov=ndna/ tests/

.PHONY: debug
debug:
	pytest -sqq tests/

.PHONY: cov
cov:
	pytest -qq --cov-report term-missing --cov=ndna/ tests/

.PHONY: docs
docs:
	rm -rf docs/html*
	sphinx-apidoc -feT ndna/ -o docs/src --templatedir docs/src/_templates
	sphinx-build -b html docs/src docs/html
