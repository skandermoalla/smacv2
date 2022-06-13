from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from os import replace

from smac.env import StarCraft2Env
import numpy as np
from absl import logging
import time

from smac.env.starcraft2.wrapper import StarCraftCapabilityEnvWrapper

logging.set_verbosity(logging.DEBUG)


def main():

    distribution_config = {
        "n_units": 5,
        "team_gen": {
            "dist_type": "all_teams",
            "unit_types": ["marine"],
            "exception_unit_types": ["medivac"],
            "weights": [0.45, 0.45, 0.1],
            "observe": True,
        },
        # "attack": {
        #     "dist_type": "per_agent_uniform",
        #     "lower_bound": 0.8,
        #     "upper_bound": 1.0,
        #     "n_units": 12,
        #     "observe": True,
        # },
        # "enemy_mask": {
        #     "dist_type": "mask",
        #     "mask_probability": 0.5,
        #     "n_enemies": 12,
        # },
        # "start_positions": {
        #     "dist_type": "surrounded_and_reflect",
        #     "p": 0.5,
        #     "n_enemies": 5,
        #     "map_x": 32,
        #     "map_y": 32,
        # }
        # "health": {
        #     "dist_type": "per_agent_uniform",
        #     "lower_bound": 0.0,
        #     "upper_bound": 0.2,
        #     "n_units": 12,
        #     "observe": True
        # },
    }
    env = StarCraftCapabilityEnvWrapper(
        capability_config=distribution_config,
        map_name="10gen_terran",
        debug=True,
        # conic_fov=True,
        obs_own_pos=True,
        obs_starcraft=True,
        obs_timestep_number=True,
    )
    # env.reset()

    env_info = env.get_env_info()

    n_actions = env_info["n_actions"]
    n_agents = env_info["n_agents"]
    cap_size = env_info["cap_shape"]

    n_episodes = 10

    print("Training episodes")
    for e in range(n_episodes):
        env.reset()
        terminated = False
        episode_reward = 0

        while not terminated:
            obs = env.get_obs()
            state = env.get_state()
            cap = env.get_capabilities()
            # env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                actions.append(action)

            reward, terminated, _ = env.step(actions)
            time.sleep(0.15)
            episode_reward += reward
        # print("Total reward in episode {} = {}".format(e, episode_reward))
    env.save_replay()


if __name__ == "__main__":
    main()
