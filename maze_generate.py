import random
import sys
from typing import Any, Dict, List, Optional, Set, Tuple
from generate_false import generate_pacman_maze
from pathfinder import find_shortest_path
from fourty_two import get_kruskal
from print_maze_txt import write_maze_txt

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
        self,
        width: int,
        height: int,
        perfect: bool = False,
        seed: Optional[int] = None
    ) -> None:
        """Creates a MazeGenerator instance with the given parameters.

        Args:
            width: Number of columns of the maze.
            height: Number of rows of the maze.
            perfect: If True, a single-path (loop-free) "perfect maze"
                is generated; if False (default), a playable,
                Pac-Man-style board with multiple independent routes
                is generated instead.
            seed: Random seed to make generation reproducible. If
                None, a different result is produced each time.
        """
        self.width = width
        self.height = height
        self.perfect = perfect
        self.flag = 0
        if seed is not None:
            random.seed(seed)
            self.flag = 1
        self.seed = seed

    def send_seed(self) -> int:
        return self.flag

    def generate_walls(self) -> Maze:
        """Creates an empty maze grid with every wall closed.

        Returns:
            A 2D list in cells[y][x] format, where every cell is
            {"N": True, "E": True, "S": True, "W": True} (i.e. all
            four directions closed).
        """
        cells: Maze = []
        for _ in range(self.height):
            row: List[Cell] = []
            for _ in range(self.width):
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

    def generate(self, config: Config, blocked_cells: BlockedCells) -> Maze:
        """Generates only the maze structure (no file/path work).

        Depending on `self.perfect`, generates either a Kruskal-based
        perfect maze or a Pac-Man-style playable maze.

        Args:
            config: Configuration dict containing keys like
                `WIDTH`/`HEIGHT`.
            blocked_cells: Set of (row, col) coordinates to leave fully
                closed, such as the "42" pattern.

        Returns:
            The generated maze in cells[y][x] format.
        """
        cells = self.generate_walls()
        if self.perfect:
            maze = get_kruskal(cells, config, blocked_cells, self.seed)
        else:
            maze = generate_pacman_maze(
                config, cells, self.width, self.height, self.seed,
                blocked_cells
            )

        return maze

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
        maze = get_kruskal(cells, config, blocked_cells, self.seed)
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
            config, cells, config["WIDTH"], config["HEIGHT"], self.seed,
            blocked_cells
        )
        shortest_path_maze = self.maze_path(maze, config)
        return maze, shortest_path_maze
