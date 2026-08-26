import sys
from typing import List, Dict, Any, Tuple

from parse_config import parse_config


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
        val |= 1
    if cell_walls.get("E", False):
        val |= 2
    if cell_walls.get("S", False):
        val |= 4
    if cell_walls.get("W", False):
        val |= 8
    return f"{val:x}"


def save_maze_to_file(
    grid: List[List[Dict[str, bool]]],
    output_filename: str,
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    path: str,
) -> None:
    """Writes the encoded maze grid and path details to the output file."""
    with open(output_filename, "w", encoding="utf-8") as file:
        for row in grid:
            row_hex = "".join(wall_to_hex(cell) for cell in row)
            file.write(row_hex + "\n")

        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        file.write(f"{path}\n")


def create_full_wall_grid(width: int, height: int) -> List[List[Dict[str, bool]]]:
    """WIDTH x HEIGHT boyutunda, her hücrenin 4 duvarı da kapalı (N,E,S,W=True)
    olan bir grid üretir. wall_to_hex bu durumda her hücre için 15 -> 'f'
    üretecektir.
    """
    grid: List[List[Dict[str, bool]]] = []
    for _ in range(height):
        row: List[Dict[str, bool]] = [
            {"N": True, "E": True, "S": True, "W": True}
            for _ in range(width)
        ]
        grid.append(row)
    return grid


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 maze.py <config_file>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config: Dict[str, Any] = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    grid = create_full_wall_grid(config["WIDTH"], config["HEIGHT"])

    save_maze_to_file(
        grid=grid,
        output_filename=config["OUTPUT_FILE"],
        entry=config["ENTRY"],
        exit_pos=config["EXIT"],
        path="",
    )

    print(f"Maze '{config['OUTPUT_FILE']}' dosyasına yazıldı.")


if __name__ == "__main__":
    main()

