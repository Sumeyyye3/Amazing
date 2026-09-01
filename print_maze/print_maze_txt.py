from typing import List, Dict, Tuple


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
    path_str: str,
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
        file.write(f"{path_str}\n")
