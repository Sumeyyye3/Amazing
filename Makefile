PYTHON = python3
PIP = pip3
POETRY = poetry
APP = maze.py config.txt

.PHONY: all install run debug clean fclean re lint lint-strict

all: run lint clean

install:
	$(PIP) install poetry
	$(POETRY) install

run:
	$(POETRY) run $(PYTHON) $(APP)

debug:
	PYTHONASYNCIODEBUG=1 $(POETRY) run $(PYTHON) -m pdb $(APP)

lint:
	$(POETRY) run flake8 config.txt *.py
	$(POETRY) run mypy maze.py *.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .build .mypy_cache

fclean: clean
	$(POETRY) env remove --all 2>/dev/null || true
	rm -rf .venv

re: fclean install