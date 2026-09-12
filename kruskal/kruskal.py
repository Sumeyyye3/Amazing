import random
from typing import List, Dict, Tuple, Optional, Set


class SetManager:
    """Set-Manager (Union-Find) data structure with path compression.

    Attributes:
        lead: Maps each (x, y) cell to the representative of its set.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes the Union-Find structure for a width x height grid.

        Every cell starts out as its own leader (its own separate set).

        Args:
            width: Number of columns in the maze grid.
            height: Number of rows in the maze grid.
        """
        # otomatik herkes kendisinin lideri ilk başta
        self.lead = {}
        for x in range(width):
            for y in range(height):
                cell = (x, y)
                self.lead[cell] = cell

    def find(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Finds the root/representative of the set containing 'cell'.

        Args:
            cell: The (x, y) cell to look up.

        Returns:
            The (x, y) coordinate of the set's representative.
        """
        if self.lead[cell] != cell:
            # en üst lideri bul
            self.lead[cell] = self.find(self.lead[cell])
        return self.lead[cell]

    def union(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """Unites sets of cell1 and cell2.

        Args:
            cell1: The (x, y) coordinate of the first cell.
            cell2: The (x, y) coordinate of the second cell.

        Returns:
            True if merged, False if already in the same set.
        """
        lead1 = self.find(cell1)
        lead2 = self.find(cell2)

        # liderler farklıysa birleştir, aynıysa birleştirme döngü olur
        if lead1 != lead2:
            self.lead[lead2] = lead1
            return True
        return False


def generate_kruskal_maze(
    cells: List[List[Dict[str, bool]]],
    width: int,
    height: int,
    seed: Optional[int],
    blocked_cells: Set[Tuple[int, int]],
) -> List[List[Dict[str, bool]]]:
    """Carves a perfect maze into `cells` using randomized Kruskal.

    Builds a list of all candidate internal walls, shuffles it, and
    knocks down a wall whenever it connects two cells that are not
    already linked (via Union-Find). This produces a random spanning
    tree over the non-blocked cells: every cell is reachable from
    every other, with no loops.

    Args:
        cells: Pre-built grid (cells[y][x]) with every wall closed.
        width: Number of columns.
        height: Number of rows.
        seed: Optional seed for reproducible generation.
        blocked_cells: Cells (in (x, y) form) to exclude entirely from
            the maze graph (e.g. the "42" pattern); their walls are
            left untouched (fully closed).

    Returns:
        The same `cells` grid, with walls carved into a spanning tree.
    """
    # cells = []  # hücrelerimiz

    if blocked_cells is None:
        blocked_cells = set()

    if seed is not None:
        random.seed(seed)

    # for _ in range(height):  # satır sayısı kadar çalışır
    #     row = []  # satır listesi oluşturur
    #     for _ in range(width):  # sütun sayısı kadar çalışır
    #         cell = {"N": True, "E": True, "S": True, "W": True}
    #         row.append(cell)
    #     cells.append(row)

    # yıkılabilecek potansiyel duvarları konumlarıyla birlikte
    # tespit edip bu listeye atıyoruz
    walls = []
    for y in range(height):  # satırlar (x, y) x:satır indexi
        for x in range(width):  # sütunlar (x, y) y:sütun indexi
            if (x, y) in blocked_cells:
                continue
            if x < width - 1 and (x + 1, y) not in blocked_cells:
                # hücre, hücre, ortakduvar, ortakduvar
                # diyoruz ki x,y nin E si ile x+1,y nin W si ortak duvar
                walls.append(((x, y), (x + 1, y), "E", "W"))
            if y < height - 1 and (x, y + 1) not in blocked_cells:
                # aynı işlemi alt üst için yaptım
                walls.append(((x, y), (x, y + 1), "S", "N"))

    # orjinal listeyi değiştiren bir method, listeyi random karıştırır
    random.shuffle(walls)

    sets = SetManager(width, height)
    for (x1, y1), (x2, y2), wall1, wall2 in walls:
        if sets.union((x1, y1), (x2, y2)):
            cells[y1][x1][wall1] = False
            cells[y2][x2][wall2] = False

    return cells
