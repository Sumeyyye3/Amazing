import sys
from typing import List, Dict, Tuple

from parse import parse_config
from kruskal import generate_kruskal_maze
from print_maze import write_maze_txt


def print_maze_ascii(cells: List[List[Dict[str, bool]]]) -> None:
    """Labirent duvarlarını terminalde ASCII karakterleriyle gösterir."""
    height = len(cells)
    width = len(cells[0])

    # Üst sınır
    print("+" + "---+" * width)

    for y in range(height):
        # Hücre içi ve Doğu (E) duvarları
        row_str = "|"
        # Güney (S) duvarları
        bottom_str = "+"

        for x in range(width):
            cell = cells[y][x]
            row_str += "   "
            row_str += "|" if cell["E"] else " "

            bottom_str += "---+" if cell["S"] else "   +"

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
    )

    #shortest_path = Senin yazdığın en kısa yol algoritmasının return ettiğii
    #string. Bu stringde yönleri içeren string return edecek NEESWNEE gibi
    write_maze_txt(
        cells,
        config["OUTPUT_FILE"],
        config["ENTRY"],
        config["EXIT"],
        "",#shortest_path gelecek buraya,ona göre maze.txtye yazdıracağız
    )

    print(f"Maze '{config['OUTPUT_FILE']}' dosyasına başarıyla yazıldı.")
    print_maze_ascii(cells)


if __name__ == "__main__":
    main()