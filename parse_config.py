import sys
from typing import Dict, Any, Tuple


def parse_coordinates(coord_str: str, key_name: str) -> Tuple[int, int]:
    """Parses 'x,y' string into a tuple of integers."""
    try:
        parts = coord_str.split(",")
        if len(parts) != 2:
            raise ValueError
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(
            f"Invalid format for {key_name}: "
            f"'{coord_str}'. Expected format: x,y"
        )


def validate_and_convert_config(raw_config: Dict[str, str]) -> Dict[str, Any]:
    """Validates required keys, converts types, and checks bounds."""
    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }
    missing_keys = required_keys - set(raw_config.keys())

    if missing_keys:
        raise ValueError(
            f"Missing mandatory configuration keys: {', '.join(missing_keys)}"
        )

    config: Dict[str, Any] = {}

    try:
        config["WIDTH"] = int(raw_config["WIDTH"])
        config["HEIGHT"] = int(raw_config["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be valid integers.")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers.")

    config["ENTRY"] = parse_coordinates(raw_config["ENTRY"], "ENTRY")
    config["EXIT"] = parse_coordinates(raw_config["EXIT"], "EXIT")

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    if not (0 <= entry_x < config["WIDTH"] and
            0 <= entry_y < config["HEIGHT"]):
        raise ValueError(
            f"ENTRY {config['ENTRY']} is out of bounds for maze size "
            f"{config['WIDTH']}x{config['HEIGHT']}."
        )

    if not (0 <= exit_x < config["WIDTH"] and 0 <= exit_y < config["HEIGHT"]):
        raise ValueError(
            f"EXIT {config['EXIT']} is out of bounds for maze size "
            f"{config['WIDTH']}x{config['HEIGHT']}."
        )

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT coordinates must be different.")

    perfect_str = raw_config["PERFECT"].lower()
    if perfect_str in ("true", "1"):
        config["PERFECT"] = True
    elif perfect_str in ("false", "0"):
        config["PERFECT"] = False
    else:
        raise ValueError(f"Invalid value for PERFECT:"
                         f" '{raw_config['PERFECT']}'")

    if not raw_config["OUTPUT_FILE"]:
        raise ValueError("OUTPUT_FILE cannot be empty.")

    config["OUTPUT_FILE"] = raw_config["OUTPUT_FILE"]

    return config


def parse_config(filepath: str) -> Dict[str, Any]:
    """Parses and validates the configuration file.

    Args:
        filepath: The path to the configuration file.

    Returns:
        A dictionary containing parsed configuration values.
    """
    raw_config: Dict[str, str] = {}

    with open(filepath, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if "#" in line:
                line = line.split("#", 1)[0]

            line = line.strip()

            if not line:
                continue

            if "=" not in line:
                raise ValueError(
                    f"Line {line_number}: Invalid format,"
                    f"missing '=' in '{line}'"
                )

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key or not value:
                raise ValueError(
                    f"Line {line_number}: Empty key or value found."
                )

            raw_config[key] = value

    return validate_and_convert_config(raw_config)


def main() -> None:
    """Main execution entry point."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_path: str = sys.argv[1]

    try:
        config_data: Dict[str, Any] = parse_config(config_path)
        print("Configuration loaded successfully:", config_data)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

    # merhabalar
