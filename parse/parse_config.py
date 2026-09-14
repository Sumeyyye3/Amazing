from typing import Dict, Any, Tuple


def parse_coordinates(coord_str: str, key_name: str) -> Tuple[int, int]:
    """Parses 'x,y' string into a tuple of integers.

    Args:
        coord_str: The raw "x,y" string to parse.
        key_name: The config key this value belongs to, used in the
            error message if parsing fails.

    Returns:
        The parsed (x, y) tuple of integers.

    Raises:
        ValueError: If `coord_str` is not in "x,y" format.
    """
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


def convert_config_types(dict_config: Dict[str, str]) -> Dict[str, Any]:
    """Checks required keys are present and converts raw string values
    to their proper types (int, tuple, bool).

    Args:
        dict_config: Raw string key/value pairs read from the
            configuration file.

    Returns:
        A dict with `WIDTH`, `HEIGHT` (int), `ENTRY`, `EXIT` (tuples),
        `PERFECT` (bool), `OUTPUT_FILE` (str), and `SEED` (int or
        None) properly typed.

    Raises:
        ValueError: If a mandatory key is missing or a value cannot
            be converted to its expected type.
    """
    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"
    }
    optional_keys = {"SEED", "PERFECT"}
    allowed_keys = required_keys | optional_keys
    missing_keys = required_keys - set(dict_config.keys())

    if missing_keys:
        raise ValueError(
            f"Missing mandatory configuration keys: {', '.join(missing_keys)}"
        )

    unexpected_keys = set(dict_config.keys()) - allowed_keys
    if unexpected_keys:
        raise ValueError(
            f"Unexpected configuration key(s):"
            f" {', '.join(sorted(unexpected_keys))}"
        )
    config: Dict[str, Any] = {}

    try:
        config["WIDTH"] = int(dict_config["WIDTH"])
        config["HEIGHT"] = int(dict_config["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be valid integers.")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers.")

    config["ENTRY"] = parse_coordinates(dict_config["ENTRY"], "ENTRY")
    config["EXIT"] = parse_coordinates(dict_config["EXIT"], "EXIT")

    perfect_str = dict_config.get("PERFECT", "").strip().lower()
    if perfect_str == "":
        config["PERFECT"] = False
    elif perfect_str in ("true", "1"):
        config["PERFECT"] = True
    elif perfect_str in ("false", "0"):
        config["PERFECT"] = False
    else:
        raise ValueError(
            f"Invalid value for PERFECT: '{dict_config['PERFECT']}'"
        )
    if not dict_config["OUTPUT_FILE"]:
        raise ValueError("OUTPUT_FILE cannot be empty.")

    config["OUTPUT_FILE"] = dict_config["OUTPUT_FILE"]
    seed_value = dict_config.get("SEED")
    if seed_value is not None and seed_value != "":
        try:
            config["SEED"] = int(seed_value)
        except ValueError:
            raise ValueError("SEED must be a valid integer.")
    else:
        config["SEED"] = None

    return config


def max_coordinat_values(config: Dict[str, Any]) -> None:
    """Checks ENTRY/EXIT are within maze bounds and differ from each other.

    Args:
        config: Configuration dict already converted to proper types,
            containing `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`.

    Raises:
        ValueError: If ENTRY or EXIT is out of bounds, or if they are
            the same coordinate.
    """
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


def validate_and_convert_config(raw_config: Dict[str, str]) -> Dict[str, Any]:
    """Validates required keys, converts types, and checks bounds.

    Args:
        raw_config: Raw string key/value pairs read from the
            configuration file.

    Returns:
        The fully validated and type-converted configuration dict.

    Raises:
        ValueError: If any key is missing, malformed, or out of bounds.
    """
    config = convert_config_types(raw_config)
    max_coordinat_values(config)
    return config


def parse_config(filepath: str) -> Dict[str, Any]:
    """Parses and validates the configuration file.

    Args:
        filepath: The path to the configuration file.

    Returns:
        A dictionary containing parsed configuration values.

    Raises:
        FileNotFoundError: If `filepath` does not exist.
        ValueError: If the file is malformed or fails validation.
    """
    key_values: Dict[str, str] = {}

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
            key = key.strip().upper()
            value = value.strip()

            if not key:
                raise ValueError(
                    f"Line {line_number}: Empty key found."
                )

            # PERFECT boş bırakılabilir; subject'e göre varsayılanı
            # False'tur. Diğer anahtarlarda boş değer hata sayılır.
            if not value and key != "PERFECT":
                raise ValueError(
                    f"Line {line_number}: Empty value found for '{key}'."
                )

            key_values[key] = value
    result_config = validate_and_convert_config(key_values)

    return result_config