import random
from typing import List, Dict, Tuple, Any, Set, Optional


class SetManager:
    """Path compression içeren Disjoint Set (Union-Find) yapısı."""

    def __init__(self, height: int, width: int, blocked_cells: Set[Tuple[int, int]]) -> None:
        self.lead = {}
        for y in range(height):
            for x in range(width):
                cell = (y, x)
                # Engelli hücreleri Union-Find kümesine dahil etmiyoruz
                if cell not in blocked_cells:
                    self.lead[cell] = cell

    def find(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Verilen hücrenin temsilcisini (liderini) bulur."""
        if self.lead[cell] != cell:
            self.lead[cell] = self.find(self.lead[cell])
        return self.lead[cell]

    def union(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """İki hücre kümesini birleştirir. Aynı kümedelerse False döner."""
        lead1 = self.find(cell1)
        lead2 = self.find(cell2)

        if lead1 != lead2:
            self.lead[lead2] = lead1
            return True
        return False


def generate_kruskal_maze(
    cells: List[List[Dict[str, bool]]],
    width: int,
    height: int,
    seed: Optional[Any] = None,
    blocked_cells: Optional[Set[Tuple[int, int]]] = None,
) -> List[List[Dict[str, bool]]]:

    if blocked_cells is None:
        blocked_cells = set()

    if seed is not None:
        random.seed(seed)

    walls = []
    # y: satır indeksi (0..height-1), x: sütun indeksi (0..width-1)
    # Hücreler (y, x) formatında işlenir.
    for y in range(height):
        for x in range(width):
            if (y, x) in blocked_cells:
                continue

            # Sağ komşu (East) ile arasındaki duvar: (y, x) ve (y, x + 1)
            if x < width - 1 and (y, x + 1) not in blocked_cells:
                walls.append(((y, x), (y, x + 1), "E", "W"))

            # Alt komşu (South) ile arasındaki duvar: (y, x) ve (y + 1, x)
            if y < height - 1 and (y + 1, x) not in blocked_cells:
                walls.append(((y, x), (y + 1, x), "S", "N"))

    # Duvarları rastgele karıştır
    random.shuffle(walls)

    # Engelli hücreleri dışarıda tutarak SetManager'ı başlat
    sets = SetManager(height, width, blocked_cells)

    for (y1, x1), (y2, x2), wall1, wall2 in walls:
        if sets.union((y1, x1), (y2, x2)):
            # Doğrudan (y, x) indekslemesiyle erişim
            cells[y1][x1][wall1] = False
            cells[y2][x2][wall2] = False

    return cells
