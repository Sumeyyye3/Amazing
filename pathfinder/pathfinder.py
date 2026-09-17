from collections import deque
from typing import Deque, Dict, List, Tuple

Cell = Dict[str, bool]
Maze = List[List[Cell]]
Coord = Tuple[int, int]

_DIRECTIONS: List[Tuple[str, int, int]] = [
    ("N", 0, -1),
    ("E", 1, 0),
    ("S", 0, 1),
    ("W", -1, 0),
]


def find_shortest_path(cells: Maze, entry: Coord, exit_pos: Coord) -> str:
    """Finds the shortest path between entry and exit using BFS.

    Since every move between two adjacent open cells has the same
    cost (1), a Breadth-First Search is enough to guarantee the
    shortest path in an unweighted maze graph.

    Args:
        cells: 2D maze grid as ``cells[y][x]``, where each cell is a
            dict with boolean walls keyed by "N", "E", "S", "W"
            (True means the wall is closed/present).
        entry: (x, y) coordinates of the entry cell.
        exit_pos: (x, y) coordinates of the exit cell.

    Returns:
        A string made of "N"/"E"/"S"/"W" letters describing the
        shortest path from entry to exit. An empty string is
        returned if entry and exit are the same cell.

    Raises:
        ValueError: If entry/exit are out of bounds, or if no path
            exists between them.
    """
    height = len(cells)
    width = len(cells[0]) if height > 0 else 0

    _validate_coordinates(entry, width, height, "ENTRY")
    _validate_coordinates(exit_pos, width, height, "EXIT")

    if entry == exit_pos:
        return ""

    visited = {entry}
    came_from: Dict[Coord, Tuple[Coord, str]] = {}
    queue: Deque[Coord] = deque([entry])

    while queue:
        current = queue.popleft()

        if current == exit_pos:
            return _rebuild_path(came_from, entry, exit_pos)

        cx, cy = current
        cell = cells[cy][cx]

        for direction, dx, dy in _DIRECTIONS:
            if cell.get(direction, True):
                continue

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
    """Raises ValueError if coord falls outside the maze bounds.

    Args:
        coord: The (x, y) coordinate to check.
        width: Number of columns of the maze.
        height: Number of rows of the maze.
        label: Name used in the error message (e.g. "ENTRY").

    Raises:
        ValueError: If `coord` is outside the [0, width) x [0, height)
            range.
    """
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
    """Walks the came_from chain backwards to build the move string.

    Args:
        came_from: Maps each visited cell to (previous cell, the
            direction taken to reach it) as recorded by the BFS.
        entry: (x, y) coordinates of the entry cell.
        exit_pos: (x, y) coordinates of the exit cell.

    Returns:
        The entry-to-exit path as a string of "N"/"E"/"S"/"W" letters.
    """
    directions: List[str] = []
    step = exit_pos

    while step != entry:
        previous, direction = came_from[step]
        directions.append(direction)
        step = previous

    directions.reverse()
    return "".join(directions)
