# AutonomousUAV - Architecture

## Overview

Path planning system for autonomous drone navigation using A* and RRT algorithms.

## Data Flow

```
Start + Goal ──→ Planning Algorithm
                    ├── A* (grid-based)
                    └── RRT / RRT* (sampling-based)
                         │
                         ▼
                   Raw Path
                         │
                         ▼
                   Path Smoothing ──→ Final Waypoints
                         │
                         ▼
                   Environment Sim ──→ Visualization
```

## Modules

### `src/planning/`
- **astar.py** - A* search algorithm on a grid map. Uses Euclidean heuristic, supports diagonal movement, and includes path smoothing via line-of-sight checking.
- **rrt.py** - RRT (Rapidly-exploring Random Tree) and RRT* algorithms for continuous space planning. RRT* adds tree rewiring for optimal paths.

### `src/simulation/`
- **environment.py** - 2D simulation environment with circular and rectangular obstacles. Includes random obstacle generation, collision detection, path visualization, and animation.

## Algorithm Comparison

| Feature | A* | RRT | RRT* |
|---------|-----|-----|------|
| Space | Grid | Continuous | Continuous |
| Optimal | Yes | No | Asymptotically |
| Speed | Fast in 2D | Medium | Slower |
| Best for | Known maps | Complex obstacles | Quality paths |
