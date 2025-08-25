"""
Tests for A* path planning algorithm.
"""

import pytest
import numpy as np
from src.planning.astar import AStarPlanner, GridMap


def test_grid_creation():
    grid = GridMap(30, 30)
    assert grid.width == 30
    assert grid.is_free(10, 10)


def test_obstacle():
    grid = GridMap(20, 20)
    grid.add_obstacle(5, 5)
    assert not grid.is_free(5, 5)
    assert grid.is_free(10, 10)


def test_find_path():
    grid = GridMap(30, 30)
    planner = AStarPlanner(grid)
    path = planner.plan(start=(0, 0), goal=(20, 20))
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (20, 20)


def test_path_around_obstacle():
    grid = GridMap(30, 30)
    for i in range(5, 25):
        grid.add_obstacle(15, i)
    planner = AStarPlanner(grid)
    path = planner.plan(start=(5, 15), goal=(25, 15))
    assert path is not None
    for x, y in path:
        assert grid.is_free(x, y)


def test_path_smoothing():
    grid = GridMap(30, 30)
    planner = AStarPlanner(grid)
    path = planner.plan(start=(0, 0), goal=(20, 20))
    smoothed = planner.smooth_path(path)
    assert len(smoothed) <= len(path)
