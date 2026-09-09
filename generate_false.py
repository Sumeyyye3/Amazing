from kruskal import generate_kruskal_maze
from typing import Optional
import random


def open_wall(cells, c1, c2, w1: str, w2: str) -> None:
    """İki komşu hücre arasındaki ortak duvarı açar (her iki taraf da)."""
    cells[c1[1]][c1[0]][w1] = False
    cells[c2[1]][c2[0]][w2] = False


def close_wall(cells, c1, c2, w1: str, w2: str) -> None:
    """Açılmış bir duvarı geri kapatır (rollback için)."""
    cells[c1[1]][c1[0]][w1] = True
    cells[c2[1]][c2[0]][w2] = True


def _window_is_fully_open(cells, left: int, top: int) -> bool:
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
    c1, c2, width: int, height: int
):
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
    cells, width, height, c1, c2
) -> bool:
    """c1-c2 arasındaki duvar açıldığında yasak "3x3 açık alan"
    oluşup oluşmadığını kontrol eder.
    """
    for left, top in _affected_windows(c1, c2, width, height):
        if _window_is_fully_open(cells, left, top):
            return True
    return False


def open_wall_count(cell) -> int:
    """Bir hücrenin kaç yönünün açık (duvarsız) olduğunu sayar."""
    return sum(1 for is_closed in cell.values() if not is_closed)


def generate_pacman_maze(
    width,
    height,
    seed: Optional,
    blocked_cells,
):
    cells = generate_kruskal_maze(width, height, seed, blocked_cells)

    # 1. Aşama: Kapalı duvarların bir kısmını kırarak döngüler (loop) oluştur
    walls = []
    for y in range(height):
        for x in range(width):
            if (x, y) in blocked_cells:
                continue
            
            if x < width - 1 and (x + 1, y) not in blocked_cells and cells[y][x]["E"]:
                walls.append(((x, y), (x + 1, y), "E", "W"))
            if y < height - 1 and (x, y + 1) not in blocked_cells and cells[y][x]["S"]:
                walls.append(((x, y), (x, y + 1), "S", "N"))

    random.shuffle(walls)
    limit = int(len(walls) * 0.15) 
    
    for c1, c2, w1, w2 in walls[:limit]:
        open_wall(cells, c1, c2, w1, w2)
        if is_three_x_three(cells, width, height, c1, c2):
            close_wall(cells, c1, c2, w1, w2)

    # 2. Aşama: Çıkmaz sokakları (Dead-ends) tespit edip yok et
    directions = {
        "N": ("S", 0, -1),
        "S": ("N", 0, 1),
        "E": ("W", 1, 0),
        "W": ("E", -1, 0)
    }
    
    while True:
        dead_ends = []
        for y in range(height):
            for x in range(width):
                if (x, y) not in blocked_cells and open_wall_count(cells[y][x]) == 1:
                    dead_ends.append((x, y))
        
        if not dead_ends:
            break
            
        removed_any = False
        for x, y in dead_ends:
            # Önceki kırma işlemlerinde bu hücre zaten açılmış olabilir, kontrol et
            if open_wall_count(cells[y][x]) != 1:
                continue 
                
            closed_walls = [w for w, is_closed in cells[y][x].items() if is_closed]
            random.shuffle(closed_walls)
            
            for w in closed_walls:
                opp_w, dx, dy = directions[w]
                nx, ny = x + dx, y + dy
                
                # Sınırların içinde mi ve engelli hücre değil mi kontrolü
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in blocked_cells:
                    open_wall(cells, (x, y), (nx, ny), w, opp_w)
                    
                    if is_three_x_three(cells, width, height, (x, y), (nx, ny)):
                        close_wall(cells, (x, y), (nx, ny), w, opp_w) # Kural bozulduysa geri al
                    else:
                        removed_any = True
                        break # Başarıyla kırıldı, diğer duvarları denemeye gerek yok
                        
        # Eğer hiçbir çıkmaz sokak kırılamadıysa (hepsi 3x3 kuralına takıldıysa) sonsuz döngüden çık
        if not removed_any:
            break 

    return cells
