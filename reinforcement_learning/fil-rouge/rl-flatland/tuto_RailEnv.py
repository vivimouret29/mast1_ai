import numpy as np
import time

from flatland.envs.rail_env import RailEnv, RailEnvActions
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.utils.rendertools import RenderTool

rail_generator = sparse_rail_generator(max_num_cities=5)

# Initialize the properties of the environment
random_env = RailEnv(
    width=50,
    height=50,
    number_of_agents=10,
    rail_generator=rail_generator,
    line_generator=sparse_line_generator(),
    obs_builder_object=GlobalObsForRailEnv()
)

# Initialize environnement renderer
env_renderer = RenderTool(random_env)

# Create a random controller to choose actions
class RandomController:
    def __init__(self, action_size):
        self.action_size = action_size

    def act(self, observations):
        actions = dict()
        for agent_handle, observation in enumerate(observations):
            action = np.random.randint(self.action_size)
            actions.update({agent_handle: action})
        return actions

# Run agent in environnement
def run_episode(env):
    controller = RandomController(env.action_space[0])
    observations, info = env.reset()

    score = 30
    actions = dict()
    n_steps = 100

    for step in range(n_steps):

        actions = controller.act(observations)
        next_observations, all_rewards, dones, info = env.step(actions)

        print("Next observations: ", next_observations)
        print("All rewards: ", all_rewards)
        print("Dones: ", dones)
        print("Infos: ", info)
        
        for agent_handle in env.get_agent_handles():
            score += all_rewards[agent_handle]

        env_renderer.render_env(show=True)
        print('Timestep {}, total score = {}'.format(step, score))

        # time.sleep(0.2)

        if dones['__all__']:
            print('All done!')
            return

    print(f"Episode didn't finish after {n_steps} timesteps.")

run_episode(random_env)