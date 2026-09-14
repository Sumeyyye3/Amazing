PYTHON = python3
PIP = pip3
POETRY = poetry
APP = a_maze_ing.py config.txt

.PHONY: all install run debug clean fclean re lint lint-strict

all: run lint clean

install:
	$(PIP) install --user --ignore-installed flake8
	$(PIP) install --user --ignore-installed mypy
	$(PIP) install --user --ignore-installed poetry
	$(POETRY) install

run:
	$(POETRY) run $(PYTHON) $(APP)

debug:
	PYTHONASYNCIODEBUG=1 $(POETRY) run $(PYTHON) -m pdb $(APP)

lint:
	flake8 --exclude=.venv .
	mypy --exclude '^\.venv/' . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	pip install build || true
	python3 -m build --outdir .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .build .mypy_cache dist
	rm -rf poetry.lock

fclean: clean
	$(POETRY) env remove --all 2>/dev/null || true
	rm -rf .venv
	rm -rf poetry.lock
	rm -rf maze.txt

re: fclean install