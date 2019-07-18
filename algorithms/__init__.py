# -*- coding: utf-8 -*-
'''
    【简介】
    PyQT5中 QThread 例子


'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
from smac.env import StarCraft2Env
import time, threading


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("QThread 例子")
        self.thread = threading.Thread(target=self.algorithm, name='LoopThread')
        self.listFile = QListWidget()
        self.btnStart = QPushButton('开始')
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)
        self.btnStart.clicked.connect(self.slotStart)

    def slotAdd(self, file_inf):

        self.listFile.addItem(file_inf)

    def slotStart(self):
        self.btnStart.setEnabled(False)
        self.thread.start()

    def algorithm(self, map_name="8m"):

        """
        强化学习算法
        :return:
        """
        print("start rl algorithm")
        env = StarCraft2Env(map_name="8m")
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

class Worker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        print("thread")
        # 线程休眠2秒
        self.sleep(1)
        self.sinOut.emit("8m")

    def algorithm(self, map_name="8m"):

        """
        强化学习算法
        :return:
        """
        print("start rl algorithm")
        env = StarCraft2Env(map_name=map_name, game_version="4.9.2")
        env_info = env.get_env_info()

        n_actions = env_info["n_actions"]
        n_agents = env_info["n_agents"]

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
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())