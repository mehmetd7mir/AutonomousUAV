"""
AutonomousUAV - Main Entry Point
-----------------------------------
Autonomous UAV path planning and navigation demo.

Usage:
    python main.py --algorithm astar
    python main.py --algorithm rrt --obstacles 20
    python main.py --demo --visualize

Author: Mehmet Demir
"""

import argparse
import numpy as np

from src.planning.astar import GridMap, AStarPlanner
from src.planning.rrt import RRTPlanner, RRTStarPlanner


def create_test_grid(width: int, height: int, num_obstacles: int) -> GridMap:
    """Create test grid with random obstacles."""
    grid = GridMap(width, height)
    grid.add_random_obstacles(num_obstacles, size=4)
    return grid


def run_astar_demo(args):
    """Run A* path planning demo."""
    print("="*50)
    print("  A* Path Planning Demo")
    print("="*50)
    print()
    
    # create grid
    grid = GridMap(args.width, args.height)
    grid.add_random_obstacles(args.obstacles, size=4)
    
    print(f"Grid size: {args.width}x{args.height}")
    print(f"Obstacles: {args.obstacles}")
    print()
    
    # create planner
    planner = AStarPlanner(grid, allow_diagonal=True)
    
    start = (5, 5)
    goal = (args.width - 10, args.height - 10)
    
    print(f"Start: {start}")
    print(f"Goal:  {goal}")
    print()
    
    # find path
    print("Searching for path...")
    path = planner.plan(start, goal)
    
    if path:
        print(f"Found path with {len(path)} waypoints")
        
        # smooth path
        smoothed = planner.smooth_path(path)
        print(f"Smoothed to {len(smoothed)} waypoints")
        
        # calculate path length
        length = sum(
            np.sqrt((smoothed[i+1][0] - smoothed[i][0])**2 +
                   (smoothed[i+1][1] - smoothed[i][1])**2)
            for i in range(len(smoothed) - 1)
        )
        print(f"Path length: {length:.1f} units")
        
        if args.visualize:
            visualize_grid_path(grid, smoothed, start, goal)
        
        return smoothed
    else:
        print("No path found!")
        return None


def run_rrt_demo(args):
    """Run RRT path planning demo."""
    print("="*50)
    print("  RRT Path Planning Demo")
    print("="*50)
    print()
    
    # create planner
    if args.rrt_star:
        print("Using RRT* (optimal variant)")
        planner = RRTStarPlanner(
            args.width, args.height,
            step_size=5.0,
            max_iterations=args.iterations
        )
    else:
        print("Using RRT")
        planner = RRTPlanner(
            args.width, args.height,
            step_size=5.0,
            max_iterations=args.iterations
        )
    
    # add obstacles
    planner.add_random_obstacles(args.obstacles, radius=6)
    
    print(f"Environment: {args.width}x{args.height}")
    print(f"Obstacles: {args.obstacles}")
    print(f"Max iterations: {args.iterations}")
    print()
    
    start = (5.0, 5.0)
    goal = (float(args.width - 10), float(args.height - 10))
    
    print(f"Start: {start}")
    print(f"Goal:  {goal}")
    print()
    
    # find path
    print("Building RRT tree...")
    path = planner.plan(start, goal)
    
    if path:
        print(f"Found path with {len(path)} waypoints")
        print(f"Tree nodes: {len(planner.nodes)}")
        
        # calculate path length
        length = sum(
            np.sqrt((path[i+1][0] - path[i][0])**2 +
                   (path[i+1][1] - path[i][1])**2)
            for i in range(len(path) - 1)
        )
        print(f"Path length: {length:.1f} units")
        
        if args.visualize:
            visualize_rrt_path(planner, path, start, goal)
        
        return path
    else:
        print("No path found!")
        return None


def visualize_grid_path(grid, path, start, goal):
    """Visualize grid and A* path."""
    try:
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # draw grid obstacles
        ax.imshow(grid.grid.T, cmap='gray_r', origin='lower',
                 extent=[0, grid.width, 0, grid.height], alpha=0.5)
        
        # draw path
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, 'b-', linewidth=2, label='Path')
        
        # start/goal
        ax.scatter([start[0]], [start[1]], c='green', s=200,
                  marker='o', label='Start', zorder=10)
        ax.scatter([goal[0]], [goal[1]], c='red', s=200,
                  marker='*', label='Goal', zorder=10)
        
        ax.set_xlim(0, grid.width)
        ax.set_ylim(0, grid.height)
        ax.set_aspect('equal')
        ax.set_title('A* Path Planning')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("astar_result.png", dpi=150)
        print("Saved visualization to astar_result.png")
        plt.show()
        
    except ImportError:
        print("Matplotlib not available")


def visualize_rrt_path(planner, path, start, goal):
    """Visualize RRT tree and path."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # draw obstacles
        for x, y, r in planner.obstacles:
            circle = Circle((x, y), r, fill=True, color='gray', alpha=0.7)
            ax.add_patch(circle)
        
        # draw tree
        for node in planner.nodes:
            if node.parent:
                ax.plot([node.x, node.parent.x], [node.y, node.parent.y],
                       'g-', linewidth=0.5, alpha=0.3)
        
        # draw path
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, 'b-', linewidth=3, label='Path')
        
        # start/goal
        ax.scatter([start[0]], [start[1]], c='green', s=200,
                  marker='o', label='Start', zorder=10)
        ax.scatter([goal[0]], [goal[1]], c='red', s=200,
                  marker='*', label='Goal', zorder=10)
        
        ax.set_xlim(0, planner.width)
        ax.set_ylim(0, planner.height)
        ax.set_aspect('equal')
        ax.set_title('RRT Path Planning')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("rrt_result.png", dpi=150)
        print("Saved visualization to rrt_result.png")
        plt.show()
        
    except ImportError:
        print("Matplotlib not available")


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous UAV Path Planning System"
    )
    parser.add_argument(
        "--algorithm", "-a",
        type=str,
        default="astar",
        choices=["astar", "rrt"],
        help="Path planning algorithm"
    )
    parser.add_argument(
        "--width", "-W",
        type=int,
        default=100,
        help="Environment width"
    )
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=100,
        help="Environment height"
    )
    parser.add_argument(
        "--obstacles", "-o",
        type=int,
        default=15,
        help="Number of obstacles"
    )
    parser.add_argument(
        "--iterations", "-i",
        type=int,
        default=3000,
        help="Max iterations for RRT"
    )
    parser.add_argument(
        "--rrt-star",
        action="store_true",
        help="Use RRT* (optimal) instead of RRT"
    )
    parser.add_argument(
        "--visualize", "-v",
        action="store_true",
        help="Show visualization"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run full demo"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        print("Running full demo with both algorithms...\n")
        
        # A* demo
        args.visualize = True
        run_astar_demo(args)
        print()
        
        # RRT demo
        run_rrt_demo(args)
        return
    
    if args.algorithm == "astar":
        run_astar_demo(args)
    else:
        run_rrt_demo(args)


if __name__ == "__main__":
    main()
