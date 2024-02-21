clean:
	rm -fr dist/ *.eggs .eggs build/ .coverage htmlcov/ .mypy_cache/ .pytest_cache/ *.log *.egg-info
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' | xargs rm -rf

test:
	pip install '.[dev]'
	python -m ruff ttbot tests
	python -m mypy ttbot
	SECRET=123 python -m pytest tests

mypy:
	pip install mypy
	python -m mypy --install-types --non-interactive ttbot

release: clean
	pip install twine build
	python -m build --sdist --wheel .
	python -m twine upload dist/*
