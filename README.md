# Maze Game

2024 · Python · Tkinter · group project, three people

Find your way out of a random maze, race a friend to the exit, or watch BFS, DFS and A* solve it.

## What it does

- A new maze every game, built with recursive backtracking. Easy, Medium or Hard: 15×15, 25×25 or 35×35.
- Move with the arrow keys or WASD.
- Two players on one keyboard: WASD against the arrow keys. First to the exit wins.
- AI solver: pick BFS, DFS or A*, show the solution path, or watch the AI walk it at the speed you set.
- Stats: moves, games won, win rate, best score.

## Run it

```
python3 main.py           # the game
python3 main.py --demo    # console demo, no window
python3 main.py --test    # quick component tests
```

Needs Tkinter, which comes with most Python installs.

## How it's built

- `maze_generator.py`: the maze grid and recursive backtracking.
- `path_solver.py`: BFS, DFS and A*.
- `player.py`: the player, the AI player, two-player mode, stats.
- `gui.py`: the Tkinter window and controls.
- `main.py`: starts the game, plus the console demo and tests.
- `utils.py`: helpers for saving games, paths and maze statistics.

## Team

Group project, three people. My part: integrating and finishing the complete codebase, debugging, and the limitations write-up. Who wrote what: [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

---

Bora Marasli · Information Technology in Mechanical Engineering, TU Berlin · [LinkedIn](https://www.linkedin.com/in/boramarasli) · [More projects](https://github.com/boramarasli)
