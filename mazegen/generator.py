"""Reusable MazeGenerator class using Kruskal algorithm."""

from typing import Any, Dict, List, Optional, Set, Tuple
from fourty_two import get_block
from generate_false import generate_pacman_maze
from kruskal.kruskal import generate_kruskal_maze
from pathfinder.pathfinder import find_shortest_path


class MazeGenerator:
    """Reusable generator for perfect and Pac-Man style mazes."""

    def __init__(
        self,
        width: int = 20,
        height: int = 15,
        seed: Optional[Any] = None,
        perfect: bool = True,
        entry: Optional[Tuple[int, int]] = None,
        exit_pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Initialize maze generator parameters.

        Args:
            width: Maze width in number of cells.
            height: Maze height in number of cells.
            seed: Seed for random generator reproducibility.
            perfect: If True, generates a perfect maze (no loops).
            entry: Optional entry coordinates (x, y).
            exit_pos: Optional exit coordinates (x, y).
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry if entry is not None else (0, 0)
        self.exit = (
            exit_pos if exit_pos is not None else (width - 1, height - 1)
        )
        self.cells: Optional[List[List[Dict[str, bool]]]] = None
        self.blocked_cells: Set[Tuple[int, int]] = set()

    def generate(self, include_42: bool = True) -> List[List[Dict[str, bool]]]:
        """Generate and return the 2D cell wall structure."""
        if include_42:
            self.blocked_cells = get_block(self.height, self.width)
        else:
            self.blocked_cells = set()

        blocked_xy = {(c, r) for r, c in self.blocked_cells}

        if self.perfect:
            self.cells = generate_kruskal_maze(
                self.width, self.height, self.seed, blocked_xy
            )
        else:
            self.cells = generate_pacman_maze(
                self.width, self.height, self.seed, blocked_xy
            )
        return self.cells

    def get_structure(self) -> List[List[Dict[str, bool]]]:
        """Return the generated 2D grid structure."""
        if self.cells is None:
            return self.generate()
        return self.cells

    def get_solution(self) -> str:
        """Calculate and return shortest path between entry and exit."""
        cells = self.get_structure()
        return find_shortest_path(cells, self.entry, self.exit)
