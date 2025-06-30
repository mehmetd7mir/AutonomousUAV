"""
RRT Path Planning Algorithm
-----------------------------
Rapidly-exploring Random Tree for path planning.

RRT is sampling-based algorithm, good for high-dimensional spaces.
It builds a tree by randomly sampling points and extending toward them.

Features:
    - Works in continuous space
    - Handles complex obstacles
    - RRT* variant for optimal paths
    - Bi-directional RRT

Author: Mehmet Demir
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RRTNode:
    """Node in RRT tree"""
    x: float
    y: float
    parent: Optional['RRTNode'] = None
    cost: float = 0.0
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class RRTPlanner:
    """
    RRT path planning algorithm.
    
    Example:
        planner = RRTPlanner(width=100, height=100)
        planner.add_obstacle(30, 30, 10)  # circular obstacle
        
        path = planner.plan((5, 5), (90, 90))
        for x, y in path:
            print(f"({x:.1f}, {y:.1f})")
    """
    
    def __init__(
        self,
        width: float,
        height: float,
        step_size: float = 5.0,
        max_iterations: int = 5000,
        goal_sample_rate: float = 0.1
    ):
        """
        Initialize RRT planner.
        
        Args:
            width: environment width
            height: environment height
            step_size: maximum step size when extending
            max_iterations: max iterations before giving up
            goal_sample_rate: probability of sampling goal directly
        """
        self.width = width
        self.height = height
        self.step_size = step_size
        self.max_iterations = max_iterations
        self.goal_sample_rate = goal_sample_rate
        
        # obstacles stored as (x, y, radius)
        self.obstacles: List[Tuple[float, float, float]] = []
        
        # tree nodes
        self.nodes: List[RRTNode] = []
    
    def add_obstacle(self, x: float, y: float, radius: float):
        """Add circular obstacle."""
        self.obstacles.append((x, y, radius))
    
    def add_random_obstacles(self, count: int, radius: float = 5.0):
        """Add random circular obstacles."""
        for _ in range(count):
            x = np.random.uniform(radius, self.width - radius)
            y = np.random.uniform(radius, self.height - radius)
            self.obstacles.append((x, y, radius))
    
    def is_collision_free(self, x: float, y: float) -> bool:
        """Check if point is collision free."""
        for ox, oy, r in self.obstacles:
            dist = np.sqrt((x - ox)**2 + (y - oy)**2)
            if dist < r:
                return False
        return True
    
    def is_path_collision_free(
        self,
        x1: float, y1: float,
        x2: float, y2: float
    ) -> bool:
        """Check if path between two points is collision free."""
        dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        steps = max(2, int(dist / 1.0))
        
        for i in range(steps + 1):
            t = i / steps
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            if not self.is_collision_free(x, y):
                return False
        
        return True
    
    def sample_random(
        self,
        goal: Tuple[float, float]
    ) -> Tuple[float, float]:
        """Sample random point, with bias toward goal."""
        if np.random.random() < self.goal_sample_rate:
            return goal
        
        x = np.random.uniform(0, self.width)
        y = np.random.uniform(0, self.height)
        return (x, y)
    
    def find_nearest(self, x: float, y: float) -> RRTNode:
        """Find nearest node in tree."""
        min_dist = float('inf')
        nearest = None
        
        for node in self.nodes:
            dist = np.sqrt((node.x - x)**2 + (node.y - y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = node
        
        return nearest
    
    def steer(
        self,
        from_node: RRTNode,
        to_x: float,
        to_y: float
    ) -> RRTNode:
        """Steer from node toward point, respecting step size."""
        dx = to_x - from_node.x
        dy = to_y - from_node.y
        dist = np.sqrt(dx**2 + dy**2)
        
        if dist < self.step_size:
            new_x, new_y = to_x, to_y
        else:
            theta = np.arctan2(dy, dx)
            new_x = from_node.x + self.step_size * np.cos(theta)
            new_y = from_node.y + self.step_size * np.sin(theta)
        
        return RRTNode(new_x, new_y, parent=from_node)
    
    def plan(
        self,
        start: Tuple[float, float],
        goal: Tuple[float, float],
        goal_threshold: float = 5.0
    ) -> List[Tuple[float, float]]:
        """
        Find path from start to goal.
        
        Args:
            start: start position
            goal: goal position
            goal_threshold: distance to consider goal reached
        
        Returns:
            Path as list of (x, y) tuples
        """
        # initialize tree with start
        start_node = RRTNode(start[0], start[1])
        self.nodes = [start_node]
        
        for i in range(self.max_iterations):
            # sample random point
            rand_x, rand_y = self.sample_random(goal)
            
            # find nearest node
            nearest = self.find_nearest(rand_x, rand_y)
            
            # steer toward random point
            new_node = self.steer(nearest, rand_x, rand_y)
            
            # check collision
            if not self.is_path_collision_free(
                nearest.x, nearest.y, new_node.x, new_node.y
            ):
                continue
            
            # add to tree
            self.nodes.append(new_node)
            
            # check if we reached goal
            dist_to_goal = np.sqrt(
                (new_node.x - goal[0])**2 + (new_node.y - goal[1])**2
            )
            
            if dist_to_goal < goal_threshold:
                # create goal node and connect
                goal_node = RRTNode(goal[0], goal[1], parent=new_node)
                self.nodes.append(goal_node)
                return self._extract_path(goal_node)
        
        print(f"RRT failed after {self.max_iterations} iterations")
        return []
    
    def _extract_path(self, goal_node: RRTNode) -> List[Tuple[float, float]]:
        """Extract path from goal to start."""
        path = []
        current = goal_node
        
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        
        path.reverse()
        return path


class RRTStarPlanner(RRTPlanner):
    """
    RRT* - Asymptotically Optimal RRT
    
    RRT* rewires the tree to find shorter paths.
    Takes longer but gives better results.
    """
    
    def __init__(
        self,
        width: float,
        height: float,
        step_size: float = 5.0,
        max_iterations: int = 5000,
        goal_sample_rate: float = 0.1,
        neighbor_radius: float = 15.0
    ):
        super().__init__(width, height, step_size, max_iterations, goal_sample_rate)
        self.neighbor_radius = neighbor_radius
    
    def find_nearby(self, x: float, y: float) -> List[RRTNode]:
        """Find all nodes within neighbor radius."""
        nearby = []
        
        for node in self.nodes:
            dist = np.sqrt((node.x - x)**2 + (node.y - y)**2)
            if dist < self.neighbor_radius:
                nearby.append(node)
        
        return nearby
    
    def get_cost(self, node: RRTNode) -> float:
        """Get cost from start to node."""
        cost = 0.0
        current = node
        
        while current.parent is not None:
            dx = current.x - current.parent.x
            dy = current.y - current.parent.y
            cost += np.sqrt(dx**2 + dy**2)
            current = current.parent
        
        return cost
    
    def plan(
        self,
        start: Tuple[float, float],
        goal: Tuple[float, float],
        goal_threshold: float = 5.0
    ) -> List[Tuple[float, float]]:
        """
        Find optimal path using RRT*.
        """
        # initialize tree
        start_node = RRTNode(start[0], start[1], cost=0.0)
        self.nodes = [start_node]
        
        best_goal_node = None
        best_cost = float('inf')
        
        for i in range(self.max_iterations):
            # sample
            rand_x, rand_y = self.sample_random(goal)
            
            # find nearest
            nearest = self.find_nearest(rand_x, rand_y)
            
            # steer
            new_node = self.steer(nearest, rand_x, rand_y)
            
            # collision check
            if not self.is_path_collision_free(
                nearest.x, nearest.y, new_node.x, new_node.y
            ):
                continue
            
            # find nearby nodes for rewiring
            nearby = self.find_nearby(new_node.x, new_node.y)
            
            # choose best parent from nearby nodes
            best_parent = nearest
            best_parent_cost = self.get_cost(nearest) + np.sqrt(
                (new_node.x - nearest.x)**2 + (new_node.y - nearest.y)**2
            )
            
            for near in nearby:
                if near == nearest:
                    continue
                
                if not self.is_path_collision_free(
                    near.x, near.y, new_node.x, new_node.y
                ):
                    continue
                
                new_cost = self.get_cost(near) + np.sqrt(
                    (new_node.x - near.x)**2 + (new_node.y - near.y)**2
                )
                
                if new_cost < best_parent_cost:
                    best_parent = near
                    best_parent_cost = new_cost
            
            new_node.parent = best_parent
            new_node.cost = best_parent_cost
            self.nodes.append(new_node)
            
            # rewire nearby nodes through new node if shorter
            for near in nearby:
                if near == new_node.parent:
                    continue
                
                if not self.is_path_collision_free(
                    new_node.x, new_node.y, near.x, near.y
                ):
                    continue
                
                new_cost = new_node.cost + np.sqrt(
                    (new_node.x - near.x)**2 + (new_node.y - near.y)**2
                )
                
                if new_cost < self.get_cost(near):
                    near.parent = new_node
                    near.cost = new_cost
            
            # check goal
            dist_to_goal = np.sqrt(
                (new_node.x - goal[0])**2 + (new_node.y - goal[1])**2
            )
            
            if dist_to_goal < goal_threshold:
                if new_node.cost < best_cost:
                    best_goal_node = new_node
                    best_cost = new_node.cost
        
        if best_goal_node:
            # add final goal node
            goal_node = RRTNode(goal[0], goal[1], parent=best_goal_node)
            return self._extract_path(goal_node)
        
        print("RRT* could not find path")
        return []


# test
if __name__ == "__main__":
    # test basic RRT
    planner = RRTPlanner(100, 100)
    planner.add_random_obstacles(10, radius=8)
    
    path = planner.plan((5, 5), (90, 90))
    
    if path:
        print(f"RRT found path with {len(path)} points")
        for i, (x, y) in enumerate(path[:5]):
            print(f"  {i}: ({x:.1f}, {y:.1f})")
    
    # test RRT*
    print("\nTesting RRT*...")
    planner_star = RRTStarPlanner(100, 100, max_iterations=2000)
    planner_star.obstacles = planner.obstacles  # use same obstacles
    
    path_star = planner_star.plan((5, 5), (90, 90))
    
    if path_star:
        print(f"RRT* found path with {len(path_star)} points")
