from PyQt5.QtCore import QThread, pyqtSignal
# from gevent.libev.corecext import async
from smac.env import StarCraft2Env
import numpy as np


class AlgorithmAgent(object):

    def __init__(self):
        super(AlgorithmAgent, self).__init__()

    def algorithm(
            self,
            map_name="8m",
            window_size_x=1418,
            window_size_y=890,
            window_loc=(5, 155),
    ):

        """
        reinforcement learning algorithm
        :param map_name: map name
        :param window_size_x: window width
        :param window_size_y: window height
        :param window_loc: window launch position
        :return:
        """
        print("start rl algorithm")
        env = StarCraft2Env(
            map_name=map_name,
            window_size_x=window_size_x,
            window_size_y=window_size_y,
            window_loc=window_loc
        )
        env_info = env.get_env_info()

        n_actions = env_info["n_actions"]
        n_agents = env_info["n_agents"]
        print("n_actions : ", n_actions)
        print("n_agents : ", n_agents)

        n_episodes = 10

        for e in range(n_episodes):
            env.reset()
            terminated = False
            episode_reward = 0

            while not terminated:
                obs = env.get_obs()
                state = env.get_state()

                actions = []
                for agent_id in range(n_agents):
                    avail_actions = env.get_avail_agent_actions(agent_id)
                    avail_actions_ind = np.nonzero(avail_actions)[0]
                    action = np.random.choice(avail_actions_ind)
                    actions.append(action)

                reward, terminated, _ = env.step(actions)
                episode_reward += reward

            print("Total reward in episode {} = {}".format(e, episode_reward))

        env.close()


if __name__ == "__main__":

    thread = AlgorithmAgent()
    thread.start()
