PYTHON = python3
PIP = pip3
POETRY = poetry
APP = maze.py config.txt
TEST = maze_analyzer.py maze.txt

.PHONY: all install run control debug clean fclean re lint

all: run control lint clean

install:
	$(PIP) install poetry
	$(POETRY) install

run:
	$(POETRY) run $(PYTHON) $(APP)

control:
	$(POETRY) run $(PYTHON) $(TEST)

debug:
	PYTHONASYNCIODEBUG=1 $(POETRY) run $(PYTHON) -m pdb $(APP)

lint:
	$(POETRY) run mypy .
	$(POETRY) run flake8 .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .build .mypy_cache

fclean: clean
	$(POETRY) env remove --all 2>/dev/null || true
	rm -rf .venv

re: fclean install