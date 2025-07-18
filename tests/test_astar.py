"""
Tests for A* path planning algorithm.
Testing on simple grids to make sure paths are found correctly.
"""

import pytest
import numpy as np
from src.planning.astar import AStarPlanner, GridMap


class TestGridMap:
    """test the grid map"""

    def test_create_grid(self):
        """should create grid with correct size"""
        grid = GridMap(50, 50)
        assert grid.width == 50
        assert grid.height == 50

    def test_add_obstacle(self):
        """adding obstacle should mark cell as blocked"""
        grid = GridMap(20, 20)
        grid.add_obstacle(5, 5)
        assert not grid.is_free(5, 5)

    def test_free_cell(self):
        """empty cell should be free"""
        grid = GridMap(20, 20)
        assert grid.is_free(10, 10)

    def test_out_of_bounds(self):
        """out of bounds should not be free"""
        grid = GridMap(20, 20)
        assert not grid.is_free(-1, 0)
        assert not grid.is_free(0, -1)
        assert not grid.is_free(20, 0)
        assert not grid.is_free(0, 20)

    def test_add_rectangle(self):
        """rectangle obstacle should block multiple cells"""
        grid = GridMap(30, 30)
        grid.add_rectangle(5, 5, 15, 15)

        # cells inside rectangle should be blocked
        assert not grid.is_free(7, 7)
        assert not grid.is_free(10, 10)

        # cells outside should be free
        assert grid.is_free(0, 0)
        assert grid.is_free(20, 20)

    def test_random_obstacles(self):
        """should add random obstacles"""
        grid = GridMap(50, 50)
        grid.add_random_obstacles(10)

        # some cells should now be blocked
        blocked = 0
        for x in range(50):
            for y in range(50):
                if not grid.is_free(x, y):
                    blocked += 1
        assert blocked > 0

    def test_is_valid(self):
        """should validate coordinates"""
        grid = GridMap(20, 20)
        assert grid.is_valid(0, 0)
        assert grid.is_valid(19, 19)
        assert not grid.is_valid(-1, 0)
        assert not grid.is_valid(20, 0)


class TestAStarPlanner:
    """test A* pathfinding"""

    def setup_method(self):
        self.grid = GridMap(30, 30)
        self.planner = AStarPlanner(self.grid)

    def test_find_path_empty_grid(self):
        """should find path in empty grid"""
        path = self.planner.plan(
            start=(0, 0), goal=(20, 20)
        )
        assert path is not None
        assert len(path) > 0

    def test_path_starts_at_start(self):
        """path should start at start position"""
        path = self.planner.plan(
            start=(0, 0), goal=(15, 15)
        )
        assert path[0] == (0, 0)

    def test_path_ends_at_goal(self):
        """path should end at goal position"""
        path = self.planner.plan(
            start=(0, 0), goal=(15, 15)
        )
        assert path[-1] == (15, 15)

    def test_path_around_obstacle(self):
        """should find path around obstacle"""
        # put a wall in the middle
        for i in range(5, 25):
            self.grid.add_obstacle(15, i)

        path = self.planner.plan(
            start=(5, 15), goal=(25, 15)
        )
        assert path is not None
        assert len(path) > 0

        # path should not go through wall
        for x, y in path:
            assert self.grid.is_free(x, y)

    def test_same_start_goal(self):
        """start == goal should return path with one point"""
        path = self.planner.plan(
            start=(5, 5), goal=(5, 5)
        )
        assert path is not None
        assert len(path) >= 1

    def test_heuristic_positive(self):
        """heuristic distance should be positive"""
        h = self.planner.heuristic(0, 0, 10, 10)
        assert h > 0

    def test_heuristic_zero_same_point(self):
        """heuristic of same point should be 0"""
        h = self.planner.heuristic(5, 5, 5, 5)
        assert h == 0

    def test_path_smooth(self):
        """smoothed path should have fewer or equal points"""
        path = self.planner.plan(
            start=(0, 0), goal=(20, 20)
        )
        smoothed = self.planner.smooth_path(path)
        assert len(smoothed) <= len(path)
