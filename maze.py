import sys
from typing import List, Dict, Tuple

from parse import parse_config
from kruskal import generate_kruskal_maze


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


def wall_to_hex(cell_walls: Dict[str, bool]) -> str:
    """Converts cell wall states to a single lowercase hexadecimal digit.

    Bit order (LSB):
    Bit 0 (1): North
    Bit 1 (2): East
    Bit 2 (4): South
    Bit 3 (8): West
    """
    val = 0
    if cell_walls.get("N", False):
        val += 1
    if cell_walls.get("E", False):
        val += 2
    if cell_walls.get("S", False):
        val += 4
    if cell_walls.get("W", False):
        val += 8
    return f"{val:x}"


def write_maze_txt(
    cells: List[List[Dict[str, bool]]],
    output_filename: str,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    path: str,
) -> None:
    """Writes the maze structure, coordinates, and path to the output file."""
    with open(output_filename, "w", encoding="utf-8") as file:
        for row in cells:
            hex_digits = []
            for coln in row:
                hex_digit = wall_to_hex(coln)
                hex_digits.append(hex_digit)
            row_hex = "".join(hex_digits)
            file.write(row_hex + "\n")

        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")
        file.write(f"{path}\n")


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

    # 2. Eskiden kullandığımız create_cells yerine Kruskal algoritmasını çağırıyoruz.
    # Varsa config dosyasındaki SEED değerini de gönderiyoruz (yoksa None gider).
    cells = generate_kruskal_maze(
        config["WIDTH"],
        config["HEIGHT"],
        config.get("SEED"),
    )

    write_maze_txt(
        cells,
        config["OUTPUT_FILE"],
        config["ENTRY"],
        config["EXIT"],
        "",  # Path (yol çözücü) eklendiğinde burası beslenecek
    )

    print(f"Maze '{config['OUTPUT_FILE']}' dosyasına başarıyla yazıldı.")
    print_maze_ascii(cells)


if __name__ == "__main__":
    main()