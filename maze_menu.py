import random
from typing import Dict, List, Optional, Tuple

from kruskal import generate_kruskal_maze
from print_maze import write_maze_txt

class Colors:
    wall_color_palette = [
        "\033[97m",
        "\033[96m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
    ]


def print_with_colored(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    wall_color: str,
    path_coords: List[Tuple[int, int]],
) -> None:
    reset = "\033[0m"
    entry_color = "\033[95m"
    exit_color = "\033[95m"
    path_color = "\033[95m"

    height = len(cells)
    width = len(cells[0])

    if path_coords:
        path_set = set(path_coords)
    else:
        path_set = set()

    print(f"{wall_color}*{'-----*' * width}{reset}")

    for x in range(height):
        row_str = f"{wall_color}|{reset}"
        bottom_str = f"{wall_color}*{reset}"

        for y in range(width):
            cell = cells[x][y]

            if (x, y) == entry:
                row_str += f"  {entry_color}\u2665{reset}  "
            elif (x, y) == exit_:
                row_str += f"  {exit_color}\u2665{reset}  "
            elif (x, y) in path_set:
                row_str += f"  {path_color}.{reset}  "
            else:
                row_str += "     "

            if cell["E"]:
                row_str += f"{wall_color}|{reset}"
            else:
                row_str += " "

            if cell["S"]:
                bottom_str += f"{wall_color}-----*{reset}"
            else:
                bottom_str += f"     {wall_color}*{reset}"

        print(row_str)
        print(bottom_str)


def path_cell_coords(
    entry: Tuple[int, int], path_str: str
) -> List[Tuple[int, int]]:
    moves: Dict[str, Tuple[int, int]] = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }
    row, col = entry
    coords = [(row, col)]
    for direction in path_str:
        drow, dcol = moves[direction]
        row, col = row + drow, col + dcol
        coords.append((row, col))
    return coords


def create_maze(config: Dict) -> List[List[Dict[str, bool]]]:
    """Rastgele yeni bir seed ile yeni bir labirent üretir."""
    new_seed = random.randint(0, 10**9)
    return generate_kruskal_maze(config["WIDTH"], config["HEIGHT"], new_seed)


def menu(config: Dict, cells: List[List[Dict[str, bool]]], shortest_path: str) -> None:
    """a_maze_ing.py'nin main() fonksiyonu ilk çizimi yaptıktan sonra
    kontrolü buraya devreder.
    """
    entry = config["ENTRY"]
    exit = config["EXIT"]
    color_index = 0
    show_path = False

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            cells = create_maze(config)
            show_path = False
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = color_index + 1
            if color_index >= len(Colors.wall_color_palette):
                color_index = 0
        elif choice == "4":
            print("Byy <3 <3 <3")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 4.")
            continue

        write_maze_txt(cells, config["OUTPUT_FILE"], entry, exit, shortest_path)

        if show_path and shortest_path:  
            shortest_coord = path_cell_coords(entry, shortest_path)
        else:
            shortest_coord = None

        print_with_colored(
            cells, entry, exit, Colors.wall_color_palette[color_index], shortest_coord
        )