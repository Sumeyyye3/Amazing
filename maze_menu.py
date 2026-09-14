"""Interactive terminal menu for the maze visualizer."""

import random
from typing import Any, Dict, List, Optional, Tuple
from fourty_two import get_block
from maze_generate import MazeGenerator


class Colors:
    """ANSI color codes for maze wall rendering.

    Attributes:
        wall_color_palette: List of ANSI escape codes cycled through
            when the user rotates the wall color in the menu.
    """

    wall_color_palette = [
        "\033[97m",
        "\033[96m",
        "\033[92m",
        "\033[93m",
        "\033[94m",
        "\033[98m",
        "\033[91m",
        "\033[95m",
        "\033[96m"
    ]


def print_with_colored(
    cells: List[List[Dict[str, bool]]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    wall_color: str,
    path_coords: Optional[List[Tuple[int, int]]],
) -> None:
    """Print the maze with colored walls, entry, exit, and solution path.

    Args:
        cells: 2D maze grid in cells[y][x] format.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        wall_color: ANSI escape code used to color the walls.
        path_coords: (row, col) coordinates of the solution path to
            highlight, or None to hide the path.
    """
    reset = "\033[0m"
    extry_exit_color = "\033[95m"
    path_color = "\033[1m\033[95m"
    number_color = "\033[1m\033[95m"

    height = len(cells)
    width = len(cells[0])

    if path_coords:
        path_set = set(path_coords)
    else:
        path_set = set()

    blocked_cells = get_block(height, width)

    entry_row_col = (entry[1], entry[0])
    exit_row_col = (exit[1], exit[0])

    print(f"{wall_color}*{'-----*' * width}{reset}")

    for x in range(height):
        row_str = f"{wall_color}|{reset}"
        bottom_str = f"{wall_color}*{reset}"

        for y in range(width):
            cell = cells[x][y]

            if (x, y) == entry_row_col:
                row_str += f"  {extry_exit_color}\u2764{reset}  "
            elif (x, y) == exit_row_col:
                row_str += f"  {extry_exit_color}\u2764{reset}  "
            elif (x, y) in path_set:
                row_str += f"  {path_color}.{reset}  "
            elif (x, y) in blocked_cells:
                row_str += f"  {number_color}\u2764{reset}  "
            else:
                row_str += "     "

            has_e_wall = (
                cell["E"]
                or (x, y) in blocked_cells
                or (y + 1 < width and (x, y + 1) in blocked_cells)
            )
            if has_e_wall:
                row_str += f"{wall_color}|{reset}"
            else:
                row_str += " "

            has_s_wall = (
                cell["S"]
                or (x, y) in blocked_cells
                or (x + 1 < height and (x + 1, y) in blocked_cells)
            )
            if has_s_wall:
                bottom_str += f"{wall_color}-----*{reset}"
            else:
                bottom_str += f"     {wall_color}*{reset}"

        print(row_str)
        print(bottom_str)


def path_cell_coords(
    entry: Tuple[int, int], path_str: str
) -> List[Tuple[int, int]]:
    """Convert path direction string (N, E, S, W) to list of coordinates.

    `entry` is given as (x, y) = (col, row); the returned coordinates
    are (row, col), matching cells[row][col] / print_with_colored.

    Args:
        entry: (x, y) coordinates of the starting cell.
        path_str: String of "N"/"E"/"S"/"W" letters describing the path.

    Returns:
        The list of (row, col) coordinates visited along the path,
        starting with `entry`'s own (row, col) position.
    """
    moves: Dict[str, Tuple[int, int]] = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1)
    }
    entry_x, entry_y = entry
    row, col = entry_y, entry_x
    coords = [(row, col)]
    for direction in path_str:
        drow, dcol = moves[direction]
        row, col = row + drow, col + dcol
        coords.append((row, col))
    return coords


def menu(
    generator
) -> None:
    """Run interactive visualizer menu loop.

    Args:
        first_maze: The already-generated maze to display first, in
            cells[y][x] format.
        config: The validated configuration dict.
        first_path: The shortest path already computed for
            `first_maze`, as a string of "N"/"E"/"S"/"W" letters.
    """
    entry = generator.config["ENTRY"]
    exit = generator.config["EXIT"]
    color_index = 0
    show_path = False
    current_path = generator.shortest_path
    maze = generator.maze

    if show_path and current_path:
        shortest_coord = path_cell_coords(entry, current_path)
    else:
        shortest_coord = None
    print_with_colored(
        maze,
        entry,
        exit,
        Colors.wall_color_palette[color_index],
        shortest_coord,
    )
    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        choice = input("Choice? (1-4): ").strip()
        blocked_cell = get_block(generator.config["HEIGHT"], generator.config["WIDTH"])
        if choice == "1":
            if not generator.flag:
                new_seed = random.randint(0, 10**9)
            else:
                new_seed = generator.config["SEED"]

            generator = MazeGenerator(new_seed)

            if generator.config["PERFECT"]:
                maze, shortest_path = generator.generate_perfect(
                    generator.config, blocked_cell
                )
            else:
                maze, shortest_path = generator.generate_not_perfect(
                    generator.config, blocked_cell
                )
            try:
                current_path = shortest_path
            except ValueError:
                current_path = ""
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

        if show_path and current_path:
            shortest_coord = path_cell_coords(entry, current_path)
        else:
            shortest_coord = None

        print_with_colored(
            maze,
            entry,
            exit,
            Colors.wall_color_palette[color_index],
            shortest_coord,
        )
