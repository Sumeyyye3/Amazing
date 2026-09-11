"""Generate imperfect (Pac-Man usable) maze from Kruskal perfect maze."""

import random
from typing import Any, Dict, List, Optional, Set, Tuple
from kruskal import generate_kruskal_maze
from fourty_two import get_kruskal

OPPOSITE: Dict[str, str] = {"N": "S", "E": "W", "S": "N", "W": "E"}
DX: Dict[str, int] = {"N": 0, "E": 1, "S": 0, "W": -1}
DY: Dict[str, int] = {"N": -1, "E": 0, "S": 1, "W": 0}


def _has_3x3_open(
    cells: List[List[Dict[str, bool]]],
    width: int,
    height: int,
) -> bool:
    """Check if there are any 3x3 open areas without internal walls."""
    for y in range(height - 2):
        for x in range(width - 2):
            is_open = True
            for i in range(3):
                for j in range(3):
                    cx, cy = x + j, y + i
                    # Check internal vertical wall (East of cx, cy)
                    if j < 2 and cells[cy][cx]["E"]:
                        is_open = False
                        break
                    # Check internal horizontal wall (South of cx, cy)
                    if i < 2 and cells[cy][cx]["S"]:
                        is_open = False
                        break
                if not is_open:
                    break
            if is_open:
                return True
    return False


def _open_wall(
    cells: List[List[Dict[str, bool]]],
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    dir1: str,
    dir2: str,
) -> None:
    """Safely open wall between two adjacent cells."""
    cells[y1][x1][dir1] = False
    cells[y2][x2][dir2] = False


def _close_wall(
    cells: List[List[Dict[str, bool]]],
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    dir1: str,
    dir2: str,
) -> None:
    """Safely close wall between two adjacent cells."""
    cells[y1][x1][dir1] = True
    cells[y2][x2][dir2] = True


def generate_pacman_maze(
    config,
    cells: List[List[Dict[str, bool]]],
    width: int,
    height: int,
    seed: Optional[Any] = None,
    blocked_cells: Optional[Set[Tuple[int, int]]] = None
) -> List[List[Dict[str, bool]]]:
    """Generate an imperfect maze usable by a Pac-Man-like game."""
    if blocked_cells is None:
        blocked_cells = set()

    cells = get_kruskal(cells,config, blocked_cells, seed)

    if seed is not None:
        random.seed(seed)

    # 1. Add loops by knocking down some internal walls
    target_loops = max(3, (width * height) // 15)
    removed_walls = 0
    attempts = 0
    max_attempts = target_loops * 50

    while removed_walls < target_loops and attempts < max_attempts:
        attempts += 1
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 1)
        
        if (cx, cy) in blocked_cells:
            continue

        # Kapalı olan ve bloklanmamış komşulara giden duvarları topla
        walls: List[Tuple[str, int, int]] = []
        for d in ("N", "E", "S", "W"):
            if cells[cy][cx][d]:  # Duvar kapalıysa
                nx, ny = cx + DX[d], cy + DY[d]
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in blocked_cells:
                        walls.append((d, nx, ny))

        if walls:
            d, nx, ny = random.choice(walls)
            _open_wall(cells, cx, cy, nx, ny, d, OPPOSITE[d])
            if _has_3x3_open(cells, width, height):
                _close_wall(cells, cx, cy, nx, ny, d, OPPOSITE[d])
            else:
                removed_walls += 1

    # 2. Reduce dead-ends as much as possible (Pac-Man requirement)
    dead_ends_to_reduce = True
    reduction_passes = 0
    while dead_ends_to_reduce and reduction_passes < 10:
        dead_ends_to_reduce = False
        reduction_passes += 1
        for y in range(height):
            for x in range(width):
                if (x, y) in blocked_cells:
                    continue
                
                # Count closed walls
                closed_count = sum(1 for d in ("N", "E", "S", "W") if cells[y][x][d])
                if closed_count == 3:  # Dead-end cell
                    possible_opens: List[Tuple[str, int, int]] = []
                    for d in ("N", "E", "S", "W"):
                        if cells[y][x][d]:
                            nx, ny = x + DX[d], y + DY[d]
                            if 0 <= nx < width and 0 <= ny < height:
                                if (nx, ny) not in blocked_cells:
                                    possible_opens.append((d, nx, ny))
                    if possible_opens:
                        d, nx, ny = random.choice(possible_opens)
                        _open_wall(cells, x, y, nx, ny, d, OPPOSITE[d])
                        if _has_3x3_open(cells, width, height):
                            _close_wall(cells, x, y, nx, ny, d, OPPOSITE[d])
                        else:
                            dead_ends_to_reduce = True

    return cells
