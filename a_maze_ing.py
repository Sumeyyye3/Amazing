import sys
from maze_menu import menu
from maze_generate import MazeGenerator


def main() -> None:
    """Read config file, generate maze, write output, and launch menu.

    Raises:
        SystemExit: If the command-line usage is wrong, or the
            configuration file is missing or invalid.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    generator = MazeGenerator()
    menu(generator)


if __name__ == "__main__":
    main()
