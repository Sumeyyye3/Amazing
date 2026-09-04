import sys
from typing import List, Dict, Tuple
from parse import parse_config
from kruskal import generate_kruskal_maze
from print_maze import write_maze_txt


class Colors:
    """ANSI escape codes for colored terminal output."""
    RESET = "\033[0m"
    WALL = "\033[36m"


def print_maze_ascii(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit: Tuple[int, int]
) -> None:
    """Displays maze walls in the terminal using ASCII characters."""

    height = len(cells)  # satır sayımız
    width = len(cells[0])  # sütun sayımız (bir satırın leni oluyor otomatik)

    print(Colors.WALL + "*" + "-----*" * width + Colors.RESET)

    for x in range(height):
        row_str = Colors.WALL + "|" + Colors.RESET  # satırın en solundaki dış duvar
        bottom_str = Colors.WALL + "*" + Colors.RESET  # alt duvar çizgisinin başlangıç köşesi

        for y in range(width):
            cell = cells[x][y]

            if (x, y) == entry or (x, y) == exit:
                row_str += "  +  "
            else:
                row_str += "     "

            if cell["E"]:
                row_str += Colors.WALL + "|" + Colors.RESET
            else:
                row_str += " "

            if cell["S"]:
                bottom_str += Colors.WALL + "-----*" + Colors.RESET
            else:
                bottom_str += "     " + Colors.WALL + "*" + Colors.RESET

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

    cells = generate_kruskal_maze(
        config["WIDTH"],
        config["HEIGHT"],
        config.get("SEED")
    )

    # shortest_path = Senin yazdığın en kısa yol algoritmasının return ettiğii
    # string. Bu stringde yönleri içeren string return edecek NEESWNEE gibi
    write_maze_txt(
        cells,
        config["OUTPUT_FILE"],
        config["ENTRY"],
        config["EXIT"],
        "",  # shortest_path gelecek buraya,ona göre maze.txtye yazdıracağız
    )

    print(f"Maze '{config['OUTPUT_FILE']}' dosyasına başarıyla yazıldı.")
    print_maze_ascii(cells, config["ENTRY"], config["EXIT"])


if __name__ == "__main__":
    main()
