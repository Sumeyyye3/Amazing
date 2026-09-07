import random
from typing import List, Dict, Tuple, Set, Any

class SetManager:
    """Yol sıkıştırmalı Disjoint Set (Union-Find) yapısı."""
    def __init__(self, width: int, height: int):
        self.lead = {(x, y): (x, y) for x in range(width) for y in range(height)}

    def find(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        if self.lead[cell] != cell:
            self.lead[cell] = self.find(self.lead[cell])
        return self.lead[cell]

    def union(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        root1 = self.find(cell1)
        root2 = self.find(cell2)
        if root1 != root2:
            self.lead[root2] = root1
            return True
        return False


def count_open_exits(cells: List[List[Dict[str, bool]]], x: int, y: int) -> int:
    """Bir hücrenin kaç yönünün açık olduğunu hesaplar."""
    return sum(1 for is_wall in cells[y][x].values() if not is_wall)


def generate_pacman_maze(
    width: int,
    height: int,
    seed: Any = None,
    blocked_cells: Set[Tuple[int, int]] = None
) -> List[List[Dict[str, bool]]]:
    if seed is not None:
        random.seed(seed)
    if blocked_cells is None:
        blocked_cells = set()

    cells = [[{"N": True, "E": True, "S": True, "W": True} for _ in range(width)] for _ in range(height)]

    def remove_wall(c1: Tuple[int, int], c2: Tuple[int, int], w1: str, w2: str) -> None:
        cells[c1[1]][c1[0]][w1] = False
        cells[c2[1]][c2[0]][w2] = False

    dirs = {"N": (0, -1, "S"), "E": (1, 0, "W"), "S": (0, 1, "N"), "W": (-1, 0, "E")}

    walls = []
    for y in range(height):
        for x in range(width):
            if (x, y) in blocked_cells:
                continue
            if x < width - 1 and (x + 1, y) not in blocked_cells:
                walls.append(((x, y), (x + 1, y), "E", "W"))
            if y < height - 1 and (x, y + 1) not in blocked_cells:
                walls.append(((x, y), (x, y + 1), "S", "N"))

    random.shuffle(walls)
    sets = SetManager(width, height)
    remaining_walls = []

    for c1, c2, w1, w2 in walls:
        if sets.union(c1, c2):
            remove_wall(c1, c2, w1, w2)
        else:
            remaining_walls.append((c1, c2, w1, w2))

    random.shuffle(remaining_walls)
    for c1, c2, w1, w2 in remaining_walls[:2]:
        remove_wall(c1, c2, w1, w2)

    critical_cells = [
        (0, 0), (width - 1, 0), 
        (0, height - 1), (width - 1, height - 1), 
        (width // 2, height // 2)
    ]

    for cx, cy in critical_cells:
        if (cx, cy) in blocked_cells:
            continue
        
        while count_open_exits(cells, cx, cy) < 2:
            candidates = []
            for w, (dx, dy, opp) in dirs.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in blocked_cells:
                    if cells[cy][cx][w]:
                        candidates.append(((cx, cy), (nx, ny), w, opp))
            
            if not candidates:
                break
            
            c1, c2, w1, w2 = random.choice(candidates)
            remove_wall(c1, c2, w1, w2)

    return cells
