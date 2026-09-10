"""Main executable file for A-Maze-ing maze generator."""

import sys
# from typing import Optional
# import random
from typing import Dict, List, Set, Tuple
from fourty_two import get_block
# from generate_false import generate_pacman_maze
from maze_menu import menu
from parse import parse_config
# from pathfinder import find_shortest_path
# from print_maze import write_maze_txt
from maze_generate import MazeGenerator



def print_maze_ascii(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    blocked: Set[Tuple[int, int]],
) -> None:
    """Print ASCII representation of the maze to stdout."""
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
                bottom_str += "     *"

        print(row_str)
        print(bottom_str)


def main() -> None:
    """Read config file, generate maze, write output, and launch menu."""
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
    except Exception as e:
        print(f"Unexpected error while reading configuration: {e}")
        sys.exit(1)

    blocked_cells = get_block(config["HEIGHT"], config["WIDTH"])
    generator = MazeGenerator(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        perfect=config['PERFECT'],
        seed=config['SEED']
        )


    maze, shortest_path = generator.generate(config, blocked_cells)
    # if config["PERFECT"]:
    #     maze = get_kruskal(config, blocked_cells, config.get("SEED"))
    # else:
    #     maze = generate_pacman_maze(
    #         config["WIDTH"],
    #         config["HEIGHT"],
    #         config.get("SEED"),
    #         blocked_cells,
    #     )

    print_maze_ascii(maze, config["ENTRY"], config["EXIT"], blocked_cells)
    menu(config)


if __name__ == "__main__":
    main()
