import random
import sys
from typing import Any, Dict, List, Set, Tuple
from generate_false import generate_pacman_maze
from pathfinder import find_shortest_path
from fourty_two import get_kruskal
from print_maze_txt import write_maze_txt
from config_process import config_proces

Cell = Dict[str, bool]
Maze = List[List[Cell]]
Config = Dict[str, Any]
BlockedCells = Set[Tuple[int, int]]


class MazeGenerator:
    """Reusable class for generating a maze, writing it to file, and
    finding the solution path.

    Wraps generating either a Kruskal-based 'perfect' maze
    (PERFECT=True) or a playable Pac-Man-style maze (PERFECT=False),
    optionally computing the shortest path and writing everything to
    the output file.
    """

    def __init__(
        self
    ) -> None:
        """Initializes a MazeGenerator instance.

        Loads and validates the configuration via `config_proces()`
        (which reads the config path from `sys.argv[1]`), determines
        the random seed to use, then immediately generates the maze
        and computes its shortest path.

        The seed is not passed around as a function argument: every
        randomized step in the pipeline (`random.shuffle` in
        kruskal.py, `random.randint`/`random.choice` in
        generate_false.py) draws from Python's shared global
        `random` module. Seeding that global state once, here,
        before any generation happens, is what makes the whole
        pipeline reproducible.

        Args:
            None (the seed, if any, is read from the `SEED` key in
                the configuration loaded via `config_proces()`).

        Returns:
            None.
        """

        config, blocked_cells = config_proces()
        self.blocked_cells = blocked_cells
        self.config = config
        self.seed = self.config.get("SEED")
        if self.seed is not None:
            random.seed(self.seed)
        else:
            self.seed = random.randint(0, 10**9)

        self.maze = self.create_frst_maze()
        self.shortest_path = self.maze_path(self.maze, self.config)

    def create_frst_maze(self) -> Maze:
        """Generates the initial maze based on the loaded configuration.

        Dispatches to `generate_perfect` if `PERFECT` is True in the
        config, otherwise to `generate_not_perfect`.

        Args:
            None (uses `self.config` and `self.blocked_cells`).

        Returns:
            Maze: The generated maze in cells[y][x] format.
        """
        if self.config["PERFECT"]:
            maze, _ = self.generate_perfect(
                self.config, self.blocked_cells
                )
        else:
            maze, _ = self.generate_not_perfect(
                self.config, self.blocked_cells
            )

        return maze

    def generate_walls(self) -> Maze:
        """Creates an empty maze grid with every wall closed.

        Returns:
            A 2D list in cells[y][x] format, where every cell is
            {"N": True, "E": True, "S": True, "W": True} (i.e. all
            four directions closed).
        """
        config = self.config
        cells: Maze = []
        for _ in range(config["HEIGHT"]):
            row: List[Cell] = []
            for _ in range(config["WIDTH"]):
                cell = {"N": True, "E": True, "S": True, "W": True}
                row.append(cell)
            cells.append(row)
        return cells

    def maze_path(self, maze: Maze, config: Config) -> str:
        """Computes the shortest path and writes the maze to file.

        If no shortest path can be found (e.g. a disconnected maze),
        continues with an empty string; if writing the output file
        fails with an OS error (e.g. a permission issue), terminates
        the program with a clear message.

        Args:
            maze: Generated maze in cells[y][x] format.
            config: Configuration dict containing the `ENTRY`, `EXIT`,
                and `OUTPUT_FILE` keys.

        Returns:
            A string of "N"/"E"/"S"/"W" letters describing the path
            from entry to exit (empty string if no path is found).
        """
        try:
            shortest_path = find_shortest_path(
                maze, config["ENTRY"], config["EXIT"]
            )
        except ValueError as e:
            print(f"Warning: {e}")
            shortest_path = ""

        try:
            write_maze_txt(
                maze,
                config["OUTPUT_FILE"],
                config["ENTRY"],
                config["EXIT"],
                shortest_path,
            )
        except OSError as e:
            out = config["OUTPUT_FILE"]
            print(f"Error writing to output file '{out}': {e}")
            sys.exit(1)

        return shortest_path

    def generate_perfect(
        self, config: Config, blocked_cells: BlockedCells
    ) -> Tuple[Maze, str]:
        """Generates a perfect (PERFECT=True) maze, computes the
        shortest path, and writes it to the output file.

        Args:
            config: Configuration dict containing keys like
                `ENTRY`, `EXIT`, `OUTPUT_FILE`.
            blocked_cells: Set of coordinates to leave fully
                closed, such as the "42" pattern.

        Returns:
            A (maze, shortest_path) tuple: the generated maze and
            the entry-to-exit path string.
        """
        cells = self.generate_walls()
        maze = get_kruskal(cells, config, blocked_cells)
        shortest_path_maze = self.maze_path(maze, config)
        return maze, shortest_path_maze

    def generate_not_perfect(
        self, config: Config, blocked_cells: BlockedCells
    ) -> Tuple[Maze, str]:
        """Generates a playable (PERFECT=False) maze, computes the
        shortest path, and writes it to the output file.

        Args:
            config: Configuration dict containing keys like
                `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`.
            blocked_cells: Set of coordinates to leave fully
                closed, such as the "42" pattern.

        Returns:
            A (maze, shortest_path) tuple: the generated maze and
            the entry-to-exit path string.
        """
        cells = self.generate_walls()
        maze = generate_pacman_maze(
            config, cells, config["WIDTH"], config["HEIGHT"], blocked_cells
        )

        shortest_path_maze = self.maze_path(maze, config)
        return maze, shortest_path_maze
