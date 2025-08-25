"""
Tests for environment simulation.
"""

import pytest
from src.simulation.environment import Environment


def test_create_environment():
    env = Environment(100, 100)
    assert env.width == 100
    assert not env.is_collision(50, 50)


def test_circular_obstacle():
    env = Environment(100, 100)
    env.add_circular_obstacle(50, 50, 10)
    assert env.is_collision(50, 50)
    assert not env.is_collision(0, 0)


def test_rectangular_obstacle():
    env = Environment(100, 100)
    env.add_rectangular_obstacle(20, 20, 10, 10)
    assert env.is_collision(25, 25)


def test_random_obstacles():
    env = Environment(100, 100)
    env.add_random_obstacles(10)
    assert len(env.obstacles) == 10
