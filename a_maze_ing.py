"""Main executable file for A-Maze-ing maze generator."""

import sys
from typing import Dict, List, Set, Tuple
from fourty_two import get_block
from maze_menu import menu
from parse import parse_config
from maze_generate import MazeGenerator


def print_maze_ascii(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    blocked: Set[Tuple[int, int]],
) -> None:
    """Print ASCII representation of the maze to stdout.

    Args:
        cells: 2D maze grid in cells[y][x] format, each cell a dict
            with boolean walls keyed by "N", "E", "S", "W".
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        blocked: (row, col) coordinates of cells to render as fully
            blocked (e.g. the "42" pattern).
    """
    height = len(cells)  # satır sayımız
    width = len(cells[0])  # sütun sayımız (bir satırın leni oluyor otomatik)

    # entry/exit (x, y) = (sütun, satır) formatında geliyor; aşağıdaki
    # döngüde x satır indeksi, y sütun indeksi, o yüzden karşılaştırmadan
    # önce (satır, sütun)'a çeviriyoruz.
    entry_row_col = (entry[1], entry[0])
    exit_row_col = (exit[1], exit[0])

    print("*" + "-----*" * width)
    for x in range(height):
        row_str = "|"  # satırın en solundaki dış duvar
        bottom_str = "*"  # alt duvar çizgisinin başlangıç köşesi

        for y in range(width):
            cell = cells[x][y]

            if (x, y) == entry_row_col:
                row_str += "  +  "
            elif (x, y) == exit_row_col:
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
    """Read config file, generate maze, write output, and launch menu.

    Raises:
        SystemExit: If the command-line usage is wrong, or the
            configuration file is missing or invalid.
    """
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
        seed=config.get('SEED', None)
    )

    if config["PERFECT"]:
        maze, shortest_path = generator.generate_perfect(
            config, blocked_cells
        )
    else:
        maze, shortest_path = generator.generate_not_perfect(
            config, blocked_cells
        )

    print_maze_ascii(maze, config["ENTRY"], config["EXIT"], blocked_cells)
    menu(maze, config, shortest_path)


if __name__ == "__main__":
    main()
