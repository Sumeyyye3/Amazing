from kruskal import generate_kruskal_maze
from typing import Dict, List, Tuple, Optional, Set


def blocks(
    config: Dict, blocked_cells: Set[Tuple[int, int]], seed: Optional[int] = None
) -> List[List[Dict[str, bool]]]:
    blocked_xy = {(col, row) for (row, col) in blocked_cells}
    return generate_kruskal_maze(
        config["WIDTH"], config["HEIGHT"], seed, blocked_xy
    )
