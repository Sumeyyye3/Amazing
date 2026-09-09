import sys
from maze_menu import menu
from typing import List, Dict, Tuple, Set
from parse import parse_config
from print_maze import write_maze_txt
from fourty_two import get_block, get_kruskal
from generate_false import generate_pacman_maze
from pathfinder import find_shortest_path


def print_maze_ascii(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    blocked: Set[Tuple[int, int]]
) -> None:

    height = len(cells)  # satır sayımız
    width = len(cells[0])  # sütun sayımız (bir satırın leni oluyor otomatik)

    print("*" + "-----*" * width)
    for x in range(height):
        row_str = "|"  # satırın en solundaki dış duvar
        bottom_str = "*"  # alt duvar çizgisinin başlangıç köşesi

        for y in range(width):
            cell = cells[x][y]

            if (x, y) == entry:
                row_str += "  +  "
            elif (x, y) == exit:
                row_str += "  +  "
            elif (x, y) in blocked:
                row_str += "  #  "
            else:
                row_str += "     "

            if cell["E"]:
                row_str += "|"
            elif (x, y) in blocked:
                row_str += "|"
            elif (y + 1 < width) and ((x, y + 1) in blocked):
                row_str += "|"
            else:
                row_str += " "

            if cell["S"]:
                bottom_str += "-----*"
            elif (x, y) in blocked:
                bottom_str += "-----*"
            elif (x + 1 < height) and ((x + 1, y) in blocked):
                bottom_str += "-----*"
            else:
                bottom_str += "     " + "*"

        print(row_str)
        print(bottom_str)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    number_cells = get_block(config["HEIGHT"], config["WIDTH"])
    if config["PERFECT"]:
        maze = get_kruskal(config, number_cells, config.get("SEED"))
    elif not config["PERFECT"]:
        maze = generate_pacman_maze(
            config["WIDTH"], config["HEIGHT"],
            config.get("SEED"), number_cells)

    shortest_path = find_shortest_path(maze, config["ENTRY"], config["EXIT"])
    # ettiğii
    # string. Bu stringde yönleri içeren string return edecek NEESWNEE gibi
    write_maze_txt(
        maze,
        config["OUTPUT_FILE"],
        config["ENTRY"],
        config["EXIT"],
        shortest_path,  # shortest_path gelecek buraya,ona göre maze.txtye
        # yazdıracağız
    )

    print_maze_ascii(
        maze, config["ENTRY"], config["EXIT"], number_cells)
    menu(config, maze, shortest_path)


if __name__ == "__main__":
    main()
