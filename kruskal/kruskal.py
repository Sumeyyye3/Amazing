import random
from typing import List, Dict, Tuple, Any


class SetManager:
    """Set-Manager (Union-Find) data structure with path compression."""

    def __init__(self, width: int, height: int) -> None:
        self.lead = {}#otomatik herkes kendisinin lideri ilk başta 
        for x in range(width):
            for y in range(height):
                cell = (x, y)
                self.lead[cell] = cell


    def find(self, cell: Tuple[int, int]) -> Tuple[int, int]:#
        """Finds the root/representative of the set containing 'cell'."""
        if self.lead[cell] != cell:
            self.lead[cell] = self.find(self.lead[cell])#en üst lideri bul
        return self.lead[cell]

    def union(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """Unites sets of cell1 and cell2.

        Returns True if merged, False if already in the same set.
        """
        lead1 = self.find(cell1)
        lead2 = self.find(cell2)

        if lead1 != lead2:#liderler farklıysa birleştir,aynıysa birleştirme döngü olur
            self.lead[lead2] = lead1
            return True
        return False


def generate_kruskal_maze(width: int, height: int) -> List[List[Dict[str, bool]]]:
    """Generates a perfect maze using Randomized Kruskal's Algorithm."""
    cells = []#hücrelerimiz
    for _ in range(height):#satır sayısı kadar çalışır
        row = []#satır listesi oluşturur
        for _ in range(width):#sütun sayısı kadar çalışır
            cell = {"N": True, "E": True, "S": True, "W": True}
            row.append(cell)
        cells.append(row)

    walls = []#yıkılabilecek potansiyel duvarları konumlarıyla birlikte
    #tespit edip bu listeye atıyoruz
    for y in range(height):#satırlar    (x, y) x:satır indexi
        for x in range(width):#sütunlar (x, y) y:sütun indexi 
            if x < width - 1:#x = width demek en sağdasın demek
                walls.append(((x, y), (x + 1, y), "E", "W"))#hücre,hücre,ortakduvar,ortakduvar
                #diyoruz ki x,y nin E si ile x+1,y nin W si ortak duvar
            if y < height - 1:#y= height demek en alttaki duvardasın demek
                walls.append(((x, y), (x, y + 1), "S", "N"))#aynı işlemi alt üst için yaptım

    random.shuffle(walls)#orjinal listeyi değiştiren bir method,listeyi random karıştırı

    for (x1, y1), (x2, y2), wall1, wall2 in walls:
        if SetManager(width, height).union((x1, y1), (x2, y2)):
            cells[y1][x1][wall1] = False
            cells[y2][x2][wall2] = False

    return cells