PYTHON = python3
PIP = pip3
POETRY = poetry
APP = a_maze_ing.py config.txt

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
	$(POETRY) run flake8 *.py
	$(POETRY) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "No flake8 or mypy errors found."
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .build .mypy_cache

fclean: clean
    rm -rf poetry.lock
	$(POETRY) env remove --all 2>/dev/null || true
	rm -rf .venv

re: fclean install