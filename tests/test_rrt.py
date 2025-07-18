"""
Tests for RRT and RRT* path planning.
"""

import pytest
import numpy as np
from src.planning.rrt import RRTPlanner, RRTStarPlanner, RRTNode


class TestRRTPlanner:
    """test basic RRT"""

    def setup_method(self):
        self.planner = RRTPlanner(
            width=50, height=50,
            step_size=3.0, max_iterations=2000
        )

    def test_create_planner(self):
        """should create planner without error"""
        assert self.planner.step_size == 3.0

    def test_find_path_empty(self):
        """should find path with no obstacles"""
        path = self.planner.plan(
            start=(5, 5), goal=(40, 40)
        )
        assert path is not None
        assert len(path) >= 2

    def test_path_start_and_goal(self):
        """path should start and end near correct positions"""
        path = self.planner.plan(
            start=(5, 5), goal=(40, 40)
        )
        if path:
            # first point should be near start
            assert abs(path[0][0] - 5) < 5
            assert abs(path[0][1] - 5) < 5

    def test_sample_random(self):
        """random sample should be within bounds"""
        x, y = self.planner.sample_random((40, 40))
        assert 0 <= x <= 50
        assert 0 <= y <= 50

    def test_steer_limits_distance(self):
        """steer should not exceed step size"""
        from_node = RRTNode(0, 0)
        new_node = self.planner.steer(from_node, 100, 100)

        dist = np.sqrt(new_node.x**2 + new_node.y**2)
        assert dist <= self.planner.step_size + 0.01

    def test_collision_free_no_obstacles(self):
        """no obstacles = always collision free"""
        result = self.planner.is_collision_free(10, 10)
        assert result is True

    def test_collision_with_obstacle(self):
        """should detect collision with obstacle"""
        self.planner.add_obstacle(10, 10, 5)
        result = self.planner.is_collision_free(10, 10)
        assert result is False

    def test_collision_free_outside_obstacle(self):
        """point outside obstacle should be free"""
        self.planner.add_obstacle(10, 10, 3)
        result = self.planner.is_collision_free(20, 20)
        assert result is True

    def test_path_avoids_obstacle(self):
        """path should not go through big obstacle"""
        self.planner.add_obstacle(25, 25, 10)

        path = self.planner.plan(
            start=(5, 5), goal=(45, 45)
        )
        if path:
            for x, y in path:
                dist = np.sqrt((x - 25)**2 + (y - 25)**2)
                assert dist > 8


class TestRRTStarPlanner:
    """test RRT* (optimized version)"""

    def setup_method(self):
        self.planner = RRTStarPlanner(
            width=50, height=50,
            step_size=3.0, max_iterations=2000
        )

    def test_find_path(self):
        """RRT* should find a path"""
        path = self.planner.plan(
            start=(5, 5), goal=(40, 40)
        )
        assert path is not None
        assert len(path) >= 2

    def test_rrt_star_finds_path_with_obstacles(self):
        """RRT* should find path even with obstacles"""
        self.planner.add_obstacle(25, 25, 8)
        path = self.planner.plan(
            start=(5, 5), goal=(45, 45)
        )
        assert path is not None
        assert len(path) >= 2
