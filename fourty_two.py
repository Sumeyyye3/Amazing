"""42 pattern positioning and Kruskal wrapper."""

import sys
from typing import Any, Dict, List, Optional, Set, Tuple
from kruskal import generate_kruskal_maze


def get_block(height: int, width: int) -> Set[Tuple[int, int]]:
    """Get the cell coordinates for the '42' pattern in the center.

    Prints a message to stderr/console if the maze size cannot
    accommodate the '42' pattern as required by the subject.

    Args:
        height: Number of rows of the maze.
        width: Number of columns of the maze.

    Returns:
        A set of (row, col) coordinates to leave fully closed so the
        "42" shape is drawn; an empty set if the maze is too small.
    """
    digit_four = [
        "X.X",
        "X.X",
        "XXX",
        "..X",
        "..X",
    ]
    digit_two = [
        "XXX",
        "..X",
        "XXX",
        "X..",
        "XXX",
    ]

    pattern_rows = []
    for row_four, row_two in zip(digit_four, digit_two):
        pattern_rows.append(row_four + "." + row_two)

    pattern_height = len(pattern_rows)
    pattern_width = len(pattern_rows[0])

    start_row = (height - pattern_height) // 2
    start_col = (width - pattern_width) // 2

    if start_row < 0 or start_col < 0:
        print(
            f"Notice: Maze dimensions ({width}x{height}) are too small "
            f"to fit the '42' pattern (requires at least "
            f"{pattern_width}x{pattern_height}). Omitting '42' pattern.",
            file=sys.stderr,
        )
        return set()

    marked_cells = set()
    for i, row in enumerate(pattern_rows):
        for j, symbol in enumerate(row):
            if symbol == "X":
                marked_cells.add((start_row + i, start_col + j))

    return marked_cells


def get_kruskal(
        cells: List[List[Dict[str, bool]]],
        config: Dict[str, Any],
        blocked_cells: Set[Tuple[int, int]],
        seed: Optional[int]
) -> List[List[Dict[str, bool]]]:
    """Generate a perfect maze using Kruskal with blocked cells.

    Args:
        cells: Pre-built grid (cells[y][x]) with every wall closed.
        config: Configuration dict containing `WIDTH` and `HEIGHT`.
        blocked_cells: Cells to leave fully closed, given as
            (row, col) coordinates (converted internally to (x, y)
            before being passed to the Kruskal generator).
        seed: Optional seed for reproducible generation.

    Returns:
        The generated maze in cells[y][x] format.
    """
    blocked_xy = set()

    for row, col in blocked_cells:
        blocked_xy.add((col, row))

    cells_kruskal = generate_kruskal_maze(
        cells, config["WIDTH"], config["HEIGHT"], seed, blocked_xy
    )

    return cells_kruskal
