import random
from typing import List, Dict, Tuple, Any


class DisjointSet:
    """Disjoint-Set (Union-Find) data structure with path compression."""

    def __init__(self, width: int, height: int) -> None:
        # Her hücre (x, y) başlangıçta kendisinin lideridir (kümesidir)
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {
            (x, y): (x, y) for x in range(width) for y in range(height)
        }

    def find(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Finds the root/representative of the set containing 'cell'."""
        if self.parent[cell] != cell:
            # Path compression: Temsilciyi doğrudan köke bağlar
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """Unites sets of cell1 and cell2.

        Returns True if merged, False if already in the same set.
        """
        root1 = self.find(cell1)
        root2 = self.find(cell2)

        if root1 != root2:
            self.parent[root2] = root1
            return True
        return False


def generate_kruskal_maze(width: int, height: int, seed: Any = None) -> List[List[Dict[str, bool]]]:
    """Generates a perfect maze using Randomized Kruskal's Algorithm."""
    if seed is not None:
        random.seed(seed)

    # 1. Başlangıçta tüm duvarları kapalı (True) grid oluştur
    cells: List[List[Dict[str, bool]]] = [
        [{"N": True, "E": True, "S": True, "W": True} for _ in range(width)]
        for _ in range(height)
    ]

    # 2. Tüm iç duvarların (edge) listesini çıkar
    # Her duvar: ((x1, y1), (x2, y2), yön1, yön2)
    walls: List[Tuple[Tuple[int, int], Tuple[int, int], str, str]] = []

    for y in range(height):
        for x in range(width):
            # Doğu duvarı (sağdaki hücre ile)
            if x < width - 1:
                walls.append(((x, y), (x + 1, y), "E", "W"))
            # Güney duvarı (aşağıdaki hücre ile)
            if y < height - 1:
                walls.append(((x, y), (x, y + 1), "S", "N"))

    # 3. Duvar listesini rastgele karıştır
    random.shuffle(walls)

    # 4. Disjoint-Set yapısını başlat
    dsu = DisjointSet(width, height)

    # 5. Duvarları gez ve farklı kümelerdeki hücreleri birleştir
    for (x1, y1), (x2, y2), dir1, dir2 in walls:
        # Eğer iki hücre farklı kümelerdeyse aradaki duvarı yık ve kümeleri birleştir
        if dsu.union((x1, y1), (x2, y2)):
            cells[y1][x1][dir1] = False
            cells[y2][x2][dir2] = False

    return cells