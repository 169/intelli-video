PYTHON_FILES=.
lint format: PYTHON_FILES=.

lint:
	poetry run ruff .
	[ "$(PYTHON_FILES)" = "" ] || poetry run ruff format $(PYTHON_FILES) --diff
	[ "$(PYTHON_FILES)" = "" ] || poetry run ruff --select I $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || poetry run mypy $(PYTHON_FILES)

format:
	[ "$(PYTHON_FILES)" = "" ] || poetry run ruff format $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || poetry run ruff --select I --fix $(PYTHON_FILES)

######################
# HELP
######################

help:
	@echo '===================='
	@echo 'format                       - run code formatters'
	@echo 'lint                         - run linters'
