"""
Tests for RRT and RRT* path planning.
"""

import pytest
import numpy as np
from src.planning.rrt import RRTPlanner, RRTStarPlanner


def test_rrt_finds_path():
    planner = RRTPlanner(width=50, height=50, step_size=3.0, max_iterations=2000)
    path = planner.plan(start=(5, 5), goal=(40, 40))
    assert path is not None
    assert len(path) >= 2


def test_collision_detection():
    planner = RRTPlanner(width=50, height=50)
    planner.add_obstacle(25, 25, 5)
    assert not planner.is_collision_free(25, 25)
    assert planner.is_collision_free(0, 0)


def test_steer_limits_distance():
    planner = RRTPlanner(width=50, height=50, step_size=3.0)
    from src.planning.rrt import RRTNode
    node = RRTNode(0, 0)
    new = planner.steer(node, 100, 100)
    dist = np.sqrt(new.x**2 + new.y**2)
    assert dist <= planner.step_size + 0.01


def test_rrt_star_finds_path():
    planner = RRTStarPlanner(width=50, height=50, step_size=3.0, max_iterations=2000)
    path = planner.plan(start=(5, 5), goal=(40, 40))
    assert path is not None
    assert len(path) >= 2
