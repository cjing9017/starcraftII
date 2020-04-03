from PyQt5.QtCore import QThread, pyqtSignal

from smac.env import StarCraft2Env
import numpy as np

import logging
from util.signal import Signal
from resource import globalInformation
from resource import strings


class AlgorithmAgent(QThread):
    trigger = pyqtSignal()
    stop = False

    def __int__(self):
        super(AlgorithmAgent, self).__init__()

    def run(self):
        self.log = logging.getLogger('StarCraftII')
        message = "start rl algorithm"
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)
        env = StarCraft2Env(
            map_name="3m",
            window_size_x=1418,
            window_size_y=890,
            window_loc=(5, 155),
        )
        env_info = env.get_env_info()

        n_actions = env_info["n_actions"]
        n_agents = env_info["n_agents"]
        message = "n_actions : {}".format(n_actions)
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)
        message = "n_agents : {}".format(n_agents)
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)

        n_episodes = 100

        for e in range(n_episodes):
            env.reset()
            terminated = False
            episode_reward = 0

            if self.stop:
                break

            while not terminated:
                obs = env.get_obs()
                state = env.get_state()

                if globalInformation.get_value(strings.IS_STOP):
                    self.stop = True
                    break

                actions = []
                for agent_id in range(n_agents):
                    avail_actions = env.get_avail_agent_actions(agent_id)
                    avail_actions_ind = np.nonzero(avail_actions)[0]
                    action = np.random.choice(avail_actions_ind)
                    actions.append(action)

                reward, terminated, _ = env.step(actions)
                episode_reward += reward

            message = "Total reward in episode {} = {}".format(e, episode_reward)
            self.log.info(message)
            Signal.get_signal().emit_signal_str(message)

        env.close()
        Signal.get_signal().emit_signal_gameover()


if __name__ == "__main__":

    thread = AlgorithmAgent()
    thread.start()
