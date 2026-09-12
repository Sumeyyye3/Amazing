from typing import List, Dict, Tuple


def wall_to_hex(cell_walls: Dict[str, bool]) -> str:
    """Converts cell wall states to a single lowercase hexadecimal digit.

    Bit order (LSB):
    Bit 0 (1): North
    Bit 1 (2): East
    Bit 2 (4): South
    Bit 3 (8): West

    Args:
        cell_walls: Dict with boolean walls keyed by "N", "E", "S", "W"
            (True means the wall is closed).

    Returns:
        A single lowercase hexadecimal digit encoding the closed walls.
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
    """Writes the maze structure, coordinates, and path to the output file.

    Args:
        cells: 2D maze grid in cells[y][x] format.
        output_filename: Path of the file to write.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        path_str: The entry-to-exit path as a string of "N"/"E"/"S"/"W"
            letters.

    Raises:
        OSError: If the file cannot be opened or written to.
    """
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
