"""
Environment Simulation Module
--------------------------------
Simulate 2D environment for UAV path planning.

Features:
    - Random obstacle generation
    - Visualization with matplotlib
    - Path animation
    - Interactive demo

Author: Mehmet Demir
"""

import numpy as np
from typing import List, Tuple, Optional

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class Environment:
    """
    2D simulation environment.
    
    Example:
        env = Environment(100, 100)
        env.add_random_obstacles(15)
        env.visualize()
    """
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.obstacles: List[Tuple[float, float, float]] = []  # circles
        self.rectangles: List[Tuple[float, float, float, float]] = []  # rects
    
    def add_circular_obstacle(self, x: float, y: float, radius: float):
        """Add circular obstacle."""
        self.obstacles.append((x, y, radius))
    
    def add_rectangular_obstacle(
        self,
        x: float, y: float,
        width: float, height: float
    ):
        """Add rectangular obstacle."""
        self.rectangles.append((x, y, width, height))
    
    def add_random_obstacles(
        self,
        count: int,
        min_radius: float = 3.0,
        max_radius: float = 8.0
    ):
        """Add random circular obstacles."""
        for _ in range(count):
            radius = np.random.uniform(min_radius, max_radius)
            x = np.random.uniform(radius, self.width - radius)
            y = np.random.uniform(radius, self.height - radius)
            self.obstacles.append((x, y, radius))
    
    def is_collision(self, x: float, y: float, safety_margin: float = 1.0) -> bool:
        """Check if point collides with any obstacle."""
        # check circles
        for ox, oy, r in self.obstacles:
            dist = np.sqrt((x - ox)**2 + (y - oy)**2)
            if dist < r + safety_margin:
                return True
        
        # check rectangles
        for rx, ry, rw, rh in self.rectangles:
            if (rx - safety_margin <= x <= rx + rw + safety_margin and
                ry - safety_margin <= y <= ry + rh + safety_margin):
                return True
        
        return False
    
    def visualize(
        self,
        path: Optional[List[Tuple[float, float]]] = None,
        start: Optional[Tuple[float, float]] = None,
        goal: Optional[Tuple[float, float]] = None,
        tree_edges: Optional[List[Tuple[float, float, float, float]]] = None,
        title: str = "Environment"
    ):
        """
        Visualize environment with optional path.
        
        Args:
            path: list of (x, y) waypoints
            start: start position
            goal: goal position
            tree_edges: RRT tree edges for visualization
            title: plot title
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # draw obstacles
        for x, y, r in self.obstacles:
            circle = Circle((x, y), r, fill=True, color='gray', alpha=0.7)
            ax.add_patch(circle)
        
        for x, y, w, h in self.rectangles:
            rect = Rectangle((x, y), w, h, fill=True, color='gray', alpha=0.7)
            ax.add_patch(rect)
        
        # draw RRT tree if provided
        if tree_edges:
            for x1, y1, x2, y2 in tree_edges:
                ax.plot([x1, x2], [y1, y2], 'g-', linewidth=0.5, alpha=0.5)
        
        # draw path
        if path:
            path_x = [p[0] for p in path]
            path_y = [p[1] for p in path]
            ax.plot(path_x, path_y, 'b-', linewidth=2, label='Path')
            ax.scatter(path_x, path_y, c='blue', s=20, zorder=5)
        
        # draw start and goal
        if start:
            ax.scatter([start[0]], [start[1]], c='green', s=200,
                      marker='o', label='Start', zorder=10)
        
        if goal:
            ax.scatter([goal[0]], [goal[1]], c='red', s=200,
                      marker='*', label='Goal', zorder=10)
        
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def animate_path(
        self,
        path: List[Tuple[float, float]],
        start: Tuple[float, float],
        goal: Tuple[float, float],
        interval: int = 100
    ):
        """Create animation of UAV following path."""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # draw static elements
        for x, y, r in self.obstacles:
            circle = Circle((x, y), r, fill=True, color='gray', alpha=0.7)
            ax.add_patch(circle)
        
        for x, y, w, h in self.rectangles:
            rect = Rectangle((x, y), w, h, fill=True, color='gray', alpha=0.7)
            ax.add_patch(rect)
        
        # draw full path (faded)
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, 'b--', linewidth=1, alpha=0.3)
        
        # start/goal markers
        ax.scatter([start[0]], [start[1]], c='green', s=200, marker='o')
        ax.scatter([goal[0]], [goal[1]], c='red', s=200, marker='*')
        
        # animated UAV marker
        uav, = ax.plot([], [], 'ko', markersize=15)
        trail, = ax.plot([], [], 'b-', linewidth=2)
        
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title("UAV Path Animation")
        
        def init():
            uav.set_data([], [])
            trail.set_data([], [])
            return uav, trail
        
        def update(frame):
            idx = min(frame, len(path) - 1)
            
            # update UAV position
            uav.set_data([path[idx][0]], [path[idx][1]])
            
            # update trail
            trail_x = [p[0] for p in path[:idx+1]]
            trail_y = [p[1] for p in path[:idx+1]]
            trail.set_data(trail_x, trail_y)
            
            return uav, trail
        
        anim = FuncAnimation(
            fig, update, frames=len(path) + 10,
            init_func=init, blit=True, interval=interval
        )
        
        plt.tight_layout()
        return anim


def run_demo():
    """Run visualization demo."""
    print("Creating environment...")
    env = Environment(100, 100)
    env.add_random_obstacles(15, min_radius=3, max_radius=8)
    
    # import planners
    from src.planning.astar import GridMap, AStarPlanner
    
    print("Running A* path planning...")
    
    # create grid from environment
    grid = GridMap(100, 100)
    for x, y, r in env.obstacles:
        # convert circular obstacle to grid obstacles
        for dx in range(int(r) * 2 + 2):
            for dy in range(int(r) * 2 + 2):
                ox = int(x - r - 1) + dx
                oy = int(y - r - 1) + dy
                if grid.is_valid(ox, oy):
                    dist = np.sqrt((ox - x)**2 + (oy - y)**2)
                    if dist <= r + 1:
                        grid.add_obstacle(ox, oy)
    
    planner = AStarPlanner(grid)
    start = (5, 5)
    goal = (90, 90)
    
    path = planner.plan(start, goal)
    
    if path:
        print(f"Found path with {len(path)} waypoints")
        smoothed = planner.smooth_path(path)
        print(f"Smoothed to {len(smoothed)} waypoints")
        
        fig = env.visualize(smoothed, start, goal, title="A* Path Planning Demo")
        plt.savefig("path_demo.png", dpi=150)
        print("Saved to path_demo.png")
        plt.show()
    else:
        print("No path found")


# test
if __name__ == "__main__":
    if MATPLOTLIB_AVAILABLE:
        run_demo()
    else:
        print("Matplotlib required for visualization")
