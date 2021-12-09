import matplotlib.pyplot as plt
import numpy as np
import time
import pprint
import sys
import torch
import PIL

from pathlib import Path
from argparse import ArgumentParser, Namespace
from collections import deque


from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import TreeObsForRailEnv
from flatland.utils.rendertools import RenderTool

from outils.observation_utils import normalize_observation
from reinforcement_learning.dddqn_policy import DDDQNPolicy

base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir))


def single_train(n_episode):
    # Parameters for the Environment
    seed = 71
    n_agents = 30
    n_cities = 30
    x_dim = 50
    y_dim = 50
    max_rails_between_cities = 5
    max_rails_in_city = 4

    # Set the seeds
    np.random.seed(seed)

    # Observation builder
    observation_tree_depth = 2
    observation_radius = 10
    observation_builder = TreeObsForRailEnv(max_depth=observation_tree_depth)

    # Exploration parameters
    eps_start = 1.0
    eps_end = 0.01
    eps_decay = 0.997  # for 2500ts

    # Initialize the properties of the environment
    env = RailEnv(
        width=x_dim,
        height=y_dim,
        number_of_agents=n_agents,
        rail_generator=sparse_rail_generator(
            max_num_cities=n_cities,
            seed=seed,
            grid_mode=True,
            max_rails_between_cities=max_rails_between_cities,
            max_rail_pairs_in_city=max_rails_in_city
        ),
        line_generator=sparse_line_generator(),
        obs_builder_object=observation_builder
    )

    env.reset(True, True)

    # Calculate the state size given the depth of the tree observation and the number of features
    n_features_per_node = env.obs_builder.observation_dim
    n_nodes = 0
    for i in range(observation_tree_depth + 1):
        n_nodes += np.power(4, i)
    state_size = n_features_per_node * n_nodes

    # The action space of flatland is 5 discrete actions
    action_size = 5

    # Max number of steps per episode
    # This is the official formula used during evaluations
    max_steps = int(100 * (env.height + env.width + (n_agents / n_cities)))

    action_dict = dict()

    # And some variables to keep track of the progress
    scores_window = deque(maxlen=100)  # TODO smooth when rendering instead
    completion_window = deque(maxlen=100)
    scores = []
    completion = []
    action_count = [0] * action_size
    agent_obs = [None] * env.get_num_agents()
    agent_prev_obs = [None] * env.get_num_agents()
    agent_prev_action = [2] * env.get_num_agents()
    update_values = False

    # Training parameters
    training_parameters = {
        'buffer_size': int(1e5),
        'batch_size': 32,
        'update_every': 8,
        'learning_rate': 0.5e-4,
        'tau': 1e-3,
        'gamma': 0.99,
        'buffer_min_size': 0,
        'hidden_size': 256,
        'use_gpu': True
    }

    # Double Dueling DQN policy
    policy = DDDQNPolicy(state_size, action_size,
                         Namespace(**training_parameters))
    record_images = False

    frame_list = []
    for episode_idx in range(n_episode):
        score = 0
        if episode_idx == n_episode - 1:
            record_images = True
        # Reset environment
        obs, info = env.reset(
            regenerate_rail=True, regenerate_schedule=True)
        if record_images:
            env_renderer = RenderTool(env, gl="PGL")
            env_renderer.reset()
            # env_renderer.set_new_rail()

        # Build agent specific observations
        for agent in env.get_agent_handles():
            if obs[agent]:
                agent_obs[agent] = normalize_observation(
                    obs[agent], observation_tree_depth, observation_radius=observation_radius)
                agent_prev_obs[agent] = agent_obs[agent].copy()

        # Run episode
        for step in range(max_steps*3 - 1):
            for agent in env.get_agent_handles():
                if info['action_required'][agent]:
                    # If an action is required, we want to store the obs at that step as well as the action
                    update_values = True
                    action = policy.act(agent_obs[agent], eps=eps_start)
                    action_count[action] += 1
                else:
                    update_values = False
                    action = 0
                action_dict.update({agent: action})

            # Environment step
            next_obs, all_rewards, done, info = env.step(action_dict)
            if record_images:
                env_renderer.render_env(
                    show=False, show_observations=False, show_predictions=True)
                frame_list.append(PIL.Image.fromarray(
                    env_renderer.gl.get_image()))

            # Update replay buffer and train agent
            for agent in range(env.get_num_agents()):
                # Only update the values when we are done or when an action was taken and thus relevant information is present
                if update_values or done[agent]:
                    policy.step(agent_prev_obs[agent], agent_prev_action[agent],
                                all_rewards[agent], agent_obs[agent], done[agent])

                    agent_prev_obs[agent] = agent_obs[agent].copy()
                    agent_prev_action[agent] = action_dict[agent]

                if next_obs[agent]:
                    agent_obs[agent] = normalize_observation(
                        next_obs[agent], observation_tree_depth, observation_radius=10)

                score += all_rewards[agent]

            if done['__all__']:
                if record_images:
                    print(done)
                    tasks_done = np.sum([int(done[idx])
                                        for idx in env.get_agent_handles()])
                    completed = tasks_done / max(1, env.get_num_agents())
                    print(completed)
                    frame_list[0].save(   # TODO optimize this
                        f"gif/flatland_agent_{episode_idx}.gif", save_all=True, append_images=frame_list[1:], duration=3, loop=0)
                    frame_list = []
                    # env_renderer.close_window()
                break

        # Epsilon decay
        eps_start = max(eps_end, eps_decay * eps_start)

        # Collection information about training
        tasks_finished = np.sum([int(done[idx])
                                for idx in env.get_agent_handles()])
        completion_window.append(tasks_finished / max(1, env.get_num_agents()))
        scores_window.append(score / (max_steps * env.get_num_agents()))
        completion.append((np.mean(completion_window)))
        scores.append(np.mean(scores_window))
        action_probs = action_count / np.sum(action_count)

        if episode_idx % 100 == 0:
            end = "\n"
            # torch.save(policy.qnetwork_local,
            #            './torch_save/agent_' + str(episode_idx) + '.pth')
            # action_count = [1] * action_size
        else:
            end = " "

        print('\rTraining {} agents on {}x{}\t Episode {}\t Average Score: {:.3f}\tDones: {:.2f}%\tEpsilon: {:.2f} \t Action Probabilities: \t {}'.format(
            env.get_num_agents(),
            x_dim, y_dim,
            episode_idx,
            np.mean(scores_window),
            100 * np.mean(completion_window),
            eps_start,
            action_probs
        ), end=end)

    # Run episode with trained policy

    obs, info = env.reset(
        regenerate_rail=True, regenerate_schedule=True)
    env_renderer.reset()
    frame_list = []
    for step in range(max_steps - 1):
        env_renderer.render_env(
            show=False, show_observations=False, show_predictions=True)
        frame_list.append(PIL.Image.fromarray(
            env_renderer.gl.get_image()))
        for agent in env.get_agent_handles():
            if obs[agent]:
                agent_obs[agent] = normalize_observation(
                    obs[agent], observation_tree_depth,
                    observation_radius=observation_radius)
            action = 0
            if info['action_required'][agent]:
                action = policy.act(agent_obs[agent], eps=0.0)
            action_dict.update({agent: action})

        obs, all_rewards, done, info = env.step(action_dict)

        for agent in env.get_agent_handles():
            score += all_rewards[agent]

        if done['__all__']:
            frame_list[0].save(f"gif/flatland_agent_trained.gif", save_all=True,  # TODO optimize this too
                               append_images=frame_list[1:], duration=3, loop=0)
            frame_list = []
            break

    normalized_score = score / (max_steps * env.get_num_agents())
    print(normalized_score)

    tasks_finished = sum(done[idx] for idx in env.get_agent_handles())
    completion = tasks_finished / max(1, env.get_num_agents())
    print(completion)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", "--n_episodes", dest="n_episodes",
                        help="number of episodes to run", default=20, type=int)
    args = parser.parse_args()

    single_train(args.n_episodes)
