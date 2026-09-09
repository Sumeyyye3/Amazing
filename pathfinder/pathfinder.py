from collections import deque
from typing import Dict, List, Tuple

Cell = Dict[str, bool]
Maze = List[List[Cell]]
Coord = Tuple[int, int]

# Her yön için (harf, dx, dy). cells[y][x] indekslemesine göre:
# N -> y azalır, S -> y artar, E -> x artar, W -> x azalır.
_DIRECTIONS: List[Tuple[str, int, int]] = [
    ("N", 0, -1),
    ("E", 1, 0),
    ("S", 0, 1),
    ("W", -1, 0),
]


def find_shortest_path(cells: Maze, entry: Coord, exit_pos: Coord) -> str:
    height = len(cells)
    width = len(cells[0]) if height > 0 else 0

    _validate_coordinates(entry, width, height, "ENTRY")
    _validate_coordinates(exit_pos, width, height, "EXIT")

    if entry == exit_pos:
        return ""

    visited = {entry}
    came_from: Dict[Coord, Tuple[Coord, str]] = {}
    queue: deque = deque([entry])

    while queue:
        current = queue.popleft()

        if current == exit_pos:
            return _rebuild_path(came_from, entry, exit_pos)

        cx, cy = current
        cell = cells[cy][cx]

        for direction, dx, dy in _DIRECTIONS:
            if cell.get(direction, True):
                continue  # duvar kapalı, bu yönden geçilemez

            neighbor = (cx + dx, cy + dy)
            if neighbor in visited:
                continue

            visited.add(neighbor)
            came_from[neighbor] = (current, direction)
            queue.append(neighbor)

    raise ValueError(
        f"No path found between entry {entry} and exit {exit_pos}."
    )


def _validate_coordinates(
    coord: Coord, width: int, height: int, label: str
) -> None:
    x, y = coord
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{label} coordinate {coord} is out of maze bounds "
            f"({width}x{height})."
        )


def _rebuild_path(
    came_from: Dict[Coord, Tuple[Coord, str]],
    entry: Coord,
    exit_pos: Coord,
) -> str:
    directions: List[str] = []
    step = exit_pos

    while step != entry:
        previous, direction = came_from[step]
        directions.append(direction)
        step = previous

    directions.reverse()
    return "".join(directions)