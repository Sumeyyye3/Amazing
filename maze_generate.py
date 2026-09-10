import random
from typing import Optional
from print_maze import write_maze_txt
from kruskal import generate_kruskal_maze
from generate_false import generate_pacman_maze
from pathfinder import find_shortest_path
from fourty_two import get_kruskal


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = False,
        seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        else:
            self.seed = seed

    def generate_walls(self):
        cells = []
        for _ in range(self.height):  # satır sayısı kadar çalışır
            row = []  # satır listesi oluşturur
            for _ in range(self.width):  # sütun sayısı kadar çalışır
                cell = {"N": True, "E": True, "S": True, "W": True}
                row.append(cell)
            cells.append(row)
        return cells


    def maze_path(maze, config):
        try:
            write_maze_txt(
                maze,
                config["OUTPUT_FILE"],
                config["ENTRY"],
                config["EXIT"],
                shortest_path,
            )
        except OSError as e:
            print(f"Error writing to output file '{config['OUTPUT_FILE']}': {e}")
            sys.exit(1)

        try:
            shortest_path = find_shortest_path(
                maze, config["ENTRY"], config["EXIT"]
            )
        except ValueError as e:
            print(f"Warning: {e}")
        shortest_path = ""

    def generate(self, config, blocked_cells,shortest_path):
        cells = self.generate_walls()
        if self.perfect:
            maze = get_kruskal(cells, config, blocked_cells, self.seed)
        elif not self.perfect:
            maze = generate_pacman_maze(cells, self.width, self.height, self.seed, blocked_cells)

        shortest_path_maze = self.maze_path(maze, config)
        return maze, shortest_path_maze

