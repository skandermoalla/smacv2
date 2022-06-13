from re import A
from smac.env.starcraft2.distributions import SurroundedPositionDistribution
import numpy as np
from unittest.mock import patch

MUT = "smac.env.starcraft2.distributions"


def test_surrounded_distribution():
    map_x = 32
    map_y = 32
    config = {"n_units": 2, "map_x": map_x, "map_y": map_y, "n_enemies": 2}

    def ones(*args, **kwargs):
        return np.ones(size=kwargs["size"])

    distribution = SurroundedPositionDistribution(config)
    distribution.rng.uniform = ones

    positions = distribution.generate()
    ally_positions = positions["ally_start_positions"]["item"]
    enemy_positions = positions["enemy_start_positions"]["item"]

    assert all(
        ally_positions == np.array([[map_x, map_y] * config["n_units"]])
    )
    assert all(enemy_positions != np.array([map_x, map_y] * config["n_units"]))
