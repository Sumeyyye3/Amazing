from kruskal import generate_kruskal_maze
from typing import Dict, List, Tuple, Optional, Set


def get_cells(height: int, width: int) -> Set[Tuple[int, int]]:
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
        return set()

    marked_cells = set()
    for i, row in enumerate(pattern_rows):
        for j, symbol in enumerate(row):
            if symbol == "X":
                marked_cells.add((start_row + i, start_col + j))

    return marked_cells


def blocks(
    config: Dict, blocked_cells: Set[Tuple[int, int]], seed: Optional[int] = None
) -> List[List[Dict[str, bool]]]:
    blocked_xy = set()
    for row, col in blocked_cells:
        blocked_xy.add((col, row))
    cells = generate_kruskal_maze(
        config["WIDTH"], config["HEIGHT"], seed, blocked_xy
    )

    return cells

