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


def blocks(
    config: Dict, blocked_cells: Set[Tuple[int, int]], seed: Optional[int] = None
) -> List[List[Dict[str, bool]]]:
    blocked_xy = {(col, row) for (row, col) in blocked_cells}
    return generate_kruskal_maze(
        config["WIDTH"], config["HEIGHT"], seed, blocked_xy
    )
