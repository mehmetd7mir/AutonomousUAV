"""
A* Path Planning Algorithm
---------------------------
Find shortest path on a grid with obstacles.

A* is one of the best algorithms for grid-based path planning.
It uses heuristic to guide search toward goal.

Features:
    - Optimal path finding
    - Obstacle avoidance
    - Diagonal movement support
    - Path smoothing

Author: Mehmet Demir
"""

import heapq
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
import numpy as np


@dataclass
class Node:
    """Node in the search tree"""
    x: int
    y: int
    g: float = float('inf')  # cost from start
    h: float = 0.0  # heuristic (estimated cost to goal)
    parent: Optional['Node'] = None
    
    @property
    def f(self) -> float:
        """Total estimated cost"""
        return self.g + self.h
    
    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class GridMap:
    """
    2D grid map with obstacles.
    
    0 = free space
    1 = obstacle
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.int8)
    
    def add_obstacle(self, x: int, y: int):
        """Add single obstacle."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1
    
    def add_rectangle(self, x1: int, y1: int, x2: int, y2: int):
        """Add rectangular obstacle."""
        x1, x2 = max(0, min(x1, x2)), min(self.width, max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(self.height, max(y1, y2))
        self.grid[y1:y2, x1:x2] = 1
    
    def add_random_obstacles(self, count: int, size: int = 3):
        """Add random obstacles."""
        for _ in range(count):
            x = np.random.randint(0, self.width - size)
            y = np.random.randint(0, self.height - size)
            self.add_rectangle(x, y, x + size, y + size)
    
    def is_free(self, x: int, y: int) -> bool:
        """Check if cell is free."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] == 0
        return False
    
    def is_valid(self, x: int, y: int) -> bool:
        """Check if coordinates are valid."""
        return 0 <= x < self.width and 0 <= y < self.height


class AStarPlanner:
    """
    A* path planning algorithm.
    
    Example:
        grid = GridMap(100, 100)
        grid.add_random_obstacles(20)
        
        planner = AStarPlanner(grid)
        path = planner.plan((5, 5), (90, 90))
        
        for x, y in path:
            print(f"Move to ({x}, {y})")
    """
    
    # 8-connected neighbors (allows diagonal movement)
    NEIGHBORS_8 = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # 4-connected neighbors (no diagonal)
    NEIGHBORS_4 = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]
    
    def __init__(
        self,
        grid: GridMap,
        allow_diagonal: bool = True
    ):
        """
        Initialize planner.
        
        Args:
            grid: the map
            allow_diagonal: allow diagonal moves
        """
        self.grid = grid
        self.allow_diagonal = allow_diagonal
        self.neighbors = self.NEIGHBORS_8 if allow_diagonal else self.NEIGHBORS_4
    
    def heuristic(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """
        Calculate heuristic (estimated distance to goal).
        
        Using Euclidean distance for better accuracy.
        """
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def get_neighbors(self, node: Node) -> List[Tuple[int, int, float]]:
        """Get valid neighboring cells with costs."""
        neighbors = []
        
        for dx, dy in self.neighbors:
            nx, ny = node.x + dx, node.y + dy
            
            if self.grid.is_free(nx, ny):
                # diagonal moves cost sqrt(2), orthogonal cost 1
                cost = np.sqrt(2) if dx != 0 and dy != 0 else 1.0
                neighbors.append((nx, ny, cost))
        
        return neighbors
    
    def plan(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Find path from start to goal.
        
        Args:
            start: (x, y) start position
            goal: (x, y) goal position
        
        Returns:
            List of (x, y) waypoints, empty if no path found
        """
        start_x, start_y = start
        goal_x, goal_y = goal
        
        # check start and goal are valid
        if not self.grid.is_free(start_x, start_y):
            print("Start position is blocked!")
            return []
        
        if not self.grid.is_free(goal_x, goal_y):
            print("Goal position is blocked!")
            return []
        
        # create start node
        start_node = Node(start_x, start_y, g=0)
        start_node.h = self.heuristic(start_x, start_y, goal_x, goal_y)
        
        # priority queue (min-heap)
        open_list = [start_node]
        heapq.heapify(open_list)
        
        # closed set
        closed_set: Set[Tuple[int, int]] = set()
        
        # node lookup
        nodes = {(start_x, start_y): start_node}
        
        while open_list:
            # get node with lowest f
            current = heapq.heappop(open_list)
            
            # check if we reached goal
            if current.x == goal_x and current.y == goal_y:
                return self._reconstruct_path(current)
            
            # add to closed set
            closed_set.add((current.x, current.y))
            
            # explore neighbors
            for nx, ny, cost in self.get_neighbors(current):
                if (nx, ny) in closed_set:
                    continue
                
                # calculate new g cost
                new_g = current.g + cost
                
                # get or create neighbor node
                if (nx, ny) in nodes:
                    neighbor = nodes[(nx, ny)]
                    if new_g < neighbor.g:
                        # found better path
                        neighbor.g = new_g
                        neighbor.parent = current
                        # need to re-add to heap
                        heapq.heappush(open_list, neighbor)
                else:
                    # new node
                    neighbor = Node(
                        nx, ny,
                        g=new_g,
                        h=self.heuristic(nx, ny, goal_x, goal_y),
                        parent=current
                    )
                    nodes[(nx, ny)] = neighbor
                    heapq.heappush(open_list, neighbor)
        
        # no path found
        print("No path found!")
        return []
    
    def _reconstruct_path(self, goal_node: Node) -> List[Tuple[int, int]]:
        """Reconstruct path from goal to start."""
        path = []
        current = goal_node
        
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        
        path.reverse()
        return path
    
    def smooth_path(
        self,
        path: List[Tuple[int, int]],
        iterations: int = 10
    ) -> List[Tuple[int, int]]:
        """
        Smooth the path to reduce zigzag.
        
        Uses simple line-of-sight checking.
        """
        if len(path) <= 2:
            return path
        
        smoothed = [path[0]]
        i = 0
        
        while i < len(path) - 1:
            # try to skip waypoints
            j = len(path) - 1
            
            while j > i + 1:
                if self._has_line_of_sight(path[i], path[j]):
                    break
                j -= 1
            
            smoothed.append(path[j])
            i = j
        
        return smoothed
    
    def _has_line_of_sight(
        self,
        p1: Tuple[int, int],
        p2: Tuple[int, int]
    ) -> bool:
        """Check if straight line between points is obstacle-free."""
        x1, y1 = p1
        x2, y2 = p2
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        steps = max(dx, dy)
        if steps == 0:
            return True
        
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            
            if not self.grid.is_free(x, y):
                return False
        
        return True


# test
if __name__ == "__main__":
    # create grid
    grid = GridMap(50, 50)
    grid.add_random_obstacles(15, size=4)
    
    # create planner
    planner = AStarPlanner(grid)
    
    # find path
    start = (2, 2)
    goal = (47, 47)
    
    path = planner.plan(start, goal)
    
    if path:
        print(f"Found path with {len(path)} waypoints")
        
        # smooth
        smoothed = planner.smooth_path(path)
        print(f"Smoothed to {len(smoothed)} waypoints")
        
        # print first few
        for i, (x, y) in enumerate(smoothed[:5]):
            print(f"  {i}: ({x}, {y})")
    else:
        print("No path found")
