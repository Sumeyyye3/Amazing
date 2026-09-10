*This project has been created as part of the 42 curriculum by sumdogan, basakall.*

# A-Maze-ing 🌀

A Python maze generator and visualizer developed as part of the 42 curriculum. The project generates both perfect (single-path, no loops) and imperfect (Pac-Man style, multi-loop) mazes using Kruskal's Algorithm and Disjoint-Set (Union-Find) structures. It features interactive terminal visualization, pathfinding, hexadecimal serialization, and a reusable Python package (`mazegen`).

---

## 📖 Description

The goal of **A-Maze-ing** is to implement an algorithmic maze generator capable of reading configuration files, creating valid connected labyrinths, finding optimal paths from start to finish, and exporting results to a standardized hexadecimal format. In addition, the core maze generation logic is decoupled into an installable, reusable package for future applications.

Key capabilities:
- **Perfect Mazes (`PERFECT=True`):** Exactly one path connects entry and exit, without any loops or isolated cells.
- **Pac-Man Style Mazes (`PERFECT=False`):** Multi-route boards with at least two independent loops, fully accessible corridors, corners and center open, and minimized dead-ends.
- **"42" Pattern:** Automatically centers a pattern of fully closed cells representing the number "42" (with graceful fallback and notification if the dimensions are too small).
- **Interactive Terminal Visualizer:** Allows regenerating mazes, toggling solution path visibility, and rotating wall colors.
- **Hexadecimal Export:** Encodes cell walls into 4-bit hexadecimal values followed by start/goal coordinates and the shortest path string (N, E, S, W).

---

## 🛠️ Instructions

### Prerequisites
- Python 3.10 or later
- Package manager (pip, uv, or poetry)

### Installation
To install project dependencies and dev tools (flake8, mypy):
```bash
make install
```

### Execution
Run the main program with a configuration file:
```bash
python3 a_maze_ing.py config.txt
```
Or using the Makefile:
```bash
make run
```

### Linting & Static Analysis
Check code compliance with flake8 and mypy:
```bash
make lint
```
For strict checking:
```bash
make lint-strict
```

### Debugging & Cleanup
To run using Python's built-in pdb debugger:
```bash
make debug
```
To clean build artifacts, caches, and temporary files:
```bash
make clean
```

---

## ⚙️ Configuration File Format

The configuration file defines maze parameters using a `KEY=VALUE` format. Lines starting with `#` are comments and empty lines are ignored.

Mandatory keys:
```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

Optional keys:
- `SEED`: Integer seed for random number generation reproducibility.

---

## 🧩 Maze Generation Algorithm

### Chosen Algorithm: Kruskal's Algorithm
We chose **Randomized Kruskal's Algorithm** with a **Disjoint-Set (Union-Find)** data structure utilizing path compression.

### Why Kruskal's Algorithm?
1. **Uniform Spanning Tree Properties:** Kruskal's algorithm naturally builds a Minimum Spanning Tree (MST) on a grid graph, guaranteeing that a perfect maze has no loops and no unreachable regions.
2. **Flexible Constraint Handling:** It allows excluding specific cells (such as the central "42" obstacle pattern) simply by omitting edges connected to those cells before running the algorithm.
3. **Reproducibility and Determinism:** Shuffling edge candidates with a seeded PRNG guarantees identical maze generation across runs.
4. **Clean Transition to Imperfect Mazes:** A Kruskal spanning tree serves as a stable base to introduce controlled loops and eliminate dead-ends for Pac-Man-style boards while strictly preventing 3x3 open areas.

---

## 📦 Code Reusability (`mazegen`)

The maze generation logic is modularized into a standalone, installable package named `mazegen`. A pre-built wheel package (`mazegen-*.whl`) and source distribution (`mazegen-*.tar.gz`) are available in the project root.

### Installing the Package
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Python API Usage Example
```python
from mazegen import MazeGenerator

# 1. Instantiate with custom parameters
generator = MazeGenerator(
    width=20,
    height=15,
    seed=42,
    perfect=True,
    entry=(0, 0),
    exit_pos=(19, 14)
)

# 2. Generate and access maze structure (2D list of cell wall dictionaries)
cells = generator.generate(include_42=True)

# 3. Access the solution path (e.g., 'EESSES...')
solution_path = generator.get_solution()
print("Solution Path:", solution_path)
```

---

## 👥 Team & Project Management

### Roles & Responsibilities
- **Sümeyye Doğan (`sumdogan`):**
  - Core Maze Generation: Kruskal algorithm implementation with path-compressed Union-Find.
  - Pattern Integration: Designing and positioning the central "42" obstacle pattern.
  - Imperfect Maze Logic: Developing loop addition and dead-end reduction for Pac-Man mode.
  - Configuration Parser: Parsing, type validation, and boundary verification of `config.txt`.

- **Barış Sakallı (`basakall`):**
  - Pathfinding: BFS-based shortest path finder computing cardinal directions (N, E, S, W).
  - Visualization: Terminal display formatting, ANSI color palettes, and interactive menu.
  - Automation & Packaging: Makefile workflow, packaging setup (`mazegen`), and static analysis.

### Anticipated Planning & Evolution
- **Initial Plan:** Focus on perfect maze generation and basic ASCII rendering first, followed by pathfinding and file export.
- **Evolution:** During testing with `maze_analyzer.py`, we identified the necessity of strict dead-end elimination and loop validation for `PERFECT=False` mode. We refactored edge operations to prevent 3x3 open areas while preserving the "42" closed cells.
- **What Worked Well:** The separation into modular packages (`kruskal`, `pathfinder`, `parse`, `print_maze`, `mazegen`) enabled parallel development and straightforward unit testing.
- **What Could Be Improved:** Initial coordinate indexing differences between row/col and x/y required careful alignment across modules.

### Tools Used
- Python 3.10+ standard libraries (`random`, `typing`, `collections`, `sys`)
- Static analysis & linting: `flake8`, `mypy`
- Build & environment tooling: `poetry`, `uv`
- Testing & validation: `maze_analyzer.py`

---

## 📚 Resources & AI Usage

### Resources
- Jamis Buck, *Mazes for Programmers: Code Your Own Twisty Little Passages*
- Graph Theory & Spanning Trees: Kruskal's Algorithm & Disjoint-Set Union (DSU) documentation
- PEP 8 (Style Guide for Python Code) & PEP 257 (Docstring Conventions)

### AI Usage Disclosure
- **Assistance Scope:** AI was utilized to audit PEP 8 / PEP 257 formatting, resolve flake8 line-length constraints, generate `mazegen` packaging metadata, and construct dead-end pruning passes compliant with `maze_analyzer.py`.
- **Review Process:** All code and logic were manually reviewed, validated with static linters, and verified using `maze_analyzer.py` test runs.

