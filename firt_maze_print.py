from typing import List, Tuple, Set, Dict


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
    height = len(cells)
    width = len(cells[0])
    entry_row_col = (entry[1], entry[0])
    exit_row_col = (exit[1], exit[0])

    print("*" + "-----*" * width)
    for x in range(height):
        row_str = "|"
        bottom_str = "*"

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
