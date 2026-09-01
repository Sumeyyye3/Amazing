# A-Maze-Ing 🌀

A Python-based perfect maze generator and visualizer built with **Kruskal's Algorithm** and **Disjoint-Set (Union-Find)** data structures. This project generates solvable, loop-free 2D mazes based on configuration files and includes an optimal pathfinder.

---

## 👥 Team & Contributions

This project was developed collaboratively as part of a group assignment:

* **Sümeyye Doğan**
  * Core Maze Generation: Implemented Kruskal's algorithm with Disjoint-Set / Union-Find.
  * Maze Engine: Designed the 2D grid structure and wall-breaking logic using Python generators (`yield`).
  * Configuration Parser: Handled `config.txt` parsing, validation, and dimension boundaries.

* **Barış Sakallı**
  * Pathfinding Algorithm: Implemented the shortest-path detection algorithm to solve generated mazes.
  * Project Automation: Configured and built the `Makefile` workflow.
  * Documentation: Drafted the initial project structure and technical `README.md`.

---

## 🚀 Features

* **Perfect Maze Generation:** Ensures every point in the maze is reachable from any other point with exactly one path (no loops, no isolated areas).
* **Kruskal's Algorithm:** Uses randomized edge removal combined with path-compressed Union-Find for high-performance set management.
* **Configurable:** Parses dynamic dimensions (`width`, `height`) and parameters via external config files.
* **Pathfinder:** Computes and highlights the shortest exit path from start to goal.
* **Generator-Based Architecture:** Employs Python `yield` generators for step-by-step state tracking and inspection.

---
