import random
from typing import Any, Dict, List, Optional, Set, Tuple

from kruskal import generate_kruskal_maze


# Her yön için (dx, dy, karşı yön). (x, y) = (sütun, satır), kruskal.py
# ile aynı konvansiyon.
_DIRECTIONS: Dict[str, Tuple[int, int, str]] = {
    "N": (0, -1, "S"),
    "E": (1, 0, "W"),
    "S": (0, 1, "N"),
    "W": (-1, 0, "E"),
}


def open_wall(cells: Maze, c1: Coord, c2: Coord, w1: str, w2: str) -> None:
    """İki komşu hücre arasındaki ortak duvarı açar (her iki taraf da)."""
    cells[c1[1]][c1[0]][w1] = False
    cells[c2[1]][c2[0]][w2] = False


def close_wall(cells: Maze, c1: Coord, c2: Coord, w1: str, w2: str) -> None:
    """Açılmış bir duvarı geri kapatır (rollback için)."""
    cells[c1[1]][c1[0]][w1] = True
    cells[c2[1]][c2[0]][w2] = True


def _window_is_fully_open(cells: Maze, left: int, top: int) -> bool:
    """(left, top) sol-üst köşeli 3x3'lük pencerenin 12 iç duvarının
    tamamen açık olup olmadığını kontrol eder.
    """
    for row in range(top, top + 3):
        for col in range(left, left + 2):
            if cells[row][col]["E"]:
                return False
    for col in range(left, left + 3):
        for row in range(top, top + 2):
            if cells[row][col]["S"]:
                return False
    return True


def _affected_windows(
    c1: Coord, c2: Coord, width: int, height: int
) -> List[Tuple[int, int]]:
    """c1 ve c2'yi birlikte içeren, grid sınırları içindeki tüm 3x3
    pencerelerin (left, top) köşelerini döndürür.
    """
    min_x, max_x = min(c1[0], c2[0]), max(c1[0], c2[0])
    min_y, max_y = min(c1[1], c2[1]), max(c1[1], c2[1])

    windows = []
    for left in range(max_x - 2, min_x + 1):
        if left < 0 or left + 2 >= width:
            continue
        for top in range(max_y - 2, min_y + 1):
            if top < 0 or top + 2 >= height:
                continue
            windows.append((left, top))
    return windows


def is_three_x_three(
    cells: Maze, width: int, height: int, c1: Coord, c2: Coord
) -> bool:
    """c1-c2 arasındaki duvar açıldığında yasak "3x3 açık alan"
    oluşup oluşmadığını kontrol eder.
    """
    for left, top in _affected_windows(c1, c2, width, height):
        if _window_is_fully_open(cells, left, top):
            return True
    return False


def open_wall_count(cell: Cell) -> int:
    """Bir hücrenin kaç yönünün açık (duvarsız) olduğunu sayar."""
    return sum(1 for is_closed in cell.values() if not is_closed)


def _ensure_open_corridor(
    cells: Maze,
    width: int,
    height: int,
    blocked: Set[Coord],
    cell: Coord,
) -> None:
    """Verilen hücrenin (köşe/merkez) dead-end olmamasını garanti eder.
    Gerekirse -3x3 kuralını bozmayan- bir duvar daha açar.
    """
    x, y = cell
    if (x, y) in blocked:
        return
    if open_wall_count(cells[y][x]) >= 2:
        return

    candidates = []
    for direction, (dx, dy, opposite) in _DIRECTIONS.items():
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height):
            continue  # dış sınır duvarı, açılamaz
        if (nx, ny) in blocked:
            continue
        if cells[y][x][direction]:
            candidates.append((direction, nx, ny, opposite))

    random.shuffle(candidates)
    for direction, nx, ny, opposite in candidates:
        cells[y][x][direction] = False
        cells[ny][nx][opposite] = False
        if is_three_x_three(cells, width, height, (x, y), (nx, ny)):
            cells[y][x][direction] = True
            cells[ny][nx][opposite] = True
            continue
        return


def generate_pacman_maze(
    width,
    height,
    seed,
    blocked_cells,
):

    cells = generate_kruskal_maze(width, height, seed, blocked_cells)

    for c1, c2, w1, w2 in cells:
        open_wall(cells, c1, c2, w1, w2)
        if is_three_x_three(cells, width, height, c1, c2):
            close_wall(cells, c1, c2, w1, w2) 

    return cells
