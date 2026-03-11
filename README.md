# Fast Trajectory Replanning
CS 4346 - Artificial Intelligence, Spring 2026

## Overview
Implementation of Repeated A* algorithms for navigating an agent through an unknown gridworld to a target, replanning as new obstacles are discovered.

## Algorithms
- Repeated Forward A*
- Repeated Backward A*
- Adaptive A*

## Project Structure
```
fast-trajectory-replanning/
    maze.py        # Grid class and maze generation
    main.py        # Entry point
    grids/         # Saved gridworlds (coming soon)
```

## Requirements
```bash
pip install numpy
```

## Usage
```bash
python3 main.py    # Generate and visualize a maze
```