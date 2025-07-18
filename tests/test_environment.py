"""
Tests for environment simulation.
"""

import pytest
from src.simulation.environment import Environment


class TestEnvironment:
    """test the simulation environment"""

    def setup_method(self):
        self.env = Environment(100, 100)

    def test_create_environment(self):
        """should create env with correct size"""
        assert self.env.width == 100
        assert self.env.height == 100

    def test_add_circular_obstacle(self):
        """should be able to add obstacle"""
        self.env.add_circular_obstacle(50, 50, 10)
        assert len(self.env.obstacles) == 1

    def test_collision_inside_circle(self):
        """point inside circle should collide"""
        self.env.add_circular_obstacle(50, 50, 10)
        assert self.env.is_collision(50, 50)
        assert self.env.is_collision(55, 50)

    def test_no_collision_outside(self):
        """point outside obstacle should not collide"""
        self.env.add_circular_obstacle(50, 50, 5)
        assert not self.env.is_collision(0, 0)
        assert not self.env.is_collision(80, 80)

    def test_random_obstacles(self):
        """should add multiple random obstacles"""
        self.env.add_random_obstacles(10)
        assert len(self.env.obstacles) == 10

    def test_empty_env_no_collision(self):
        """empty environment should have no collisions"""
        assert not self.env.is_collision(50, 50)
        assert not self.env.is_collision(0, 0)

    def test_add_rectangular_obstacle(self):
        """should add rectangular obstacle"""
        self.env.add_rectangular_obstacle(20, 20, 10, 10)
        # check collision inside rectangle area
        assert self.env.is_collision(25, 25)
