from fourty_two import get_block
from parse import parse_config
from typing import Any
import sys


def config_proces() -> tuple[dict[str, Any], set[tuple[int, int]]]:
    """
    Reads the config file path from sys.argv[1], parses and validates it,
    and returns the config along with cells blocked by the '42' pattern.

    Takes no parameters; reads the config path from sys.argv[1] instead.

    Exits the program (sys.exit(1)) if:
        - the config file is not found or invalid,
        - the maze size can't support PERFECT=False (needs >= 2 loops),
        - ENTRY or EXIT falls inside a blocked '42' pattern cell.

    Returns:
        tuple:
            - config (dict): Parsed config with keys WIDTH, HEIGHT,
              PERFECT, ENTRY, EXIT.
            - blocked_cells: Set/list of (row, col) cells blocked by
              the '42' pattern.
    """

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

    max_possible_loops = (config["WIDTH"] - 1) * (config["HEIGHT"] - 1)
    if not config["PERFECT"] and max_possible_loops < 2:
        print(
            "Configuration error: maze size "
            f"{config['WIDTH']}x{config['HEIGHT']} is too small for "
            "PERFECT=False (a playable board needs at least two "
            "independent loops, which this size can never provide). "
            "Use a larger maze or set PERFECT=True."
        )
        sys.exit(1)

    blocked_cells = get_block(config["HEIGHT"], config["WIDTH"])

    entry_row_col = (config["ENTRY"][1], config["ENTRY"][0])
    exit_row_col = (config["EXIT"][1], config["EXIT"][0])

    if entry_row_col in blocked_cells:
        print(
            f"Configuration error: ENTRY {config['ENTRY']} falls "
            "inside the '42' pattern."
        )
        sys.exit(1)

    if exit_row_col in blocked_cells:
        print(
            f"Configuration error: EXIT {config['EXIT']} falls "
            "inside the '42' pattern."
        )
        sys.exit(1)

    return config, blocked_cells
