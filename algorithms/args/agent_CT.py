import numpy as np
import torch as th
from torch.distributions import Categorical

from .brain.mamory import Leader_Memmory
from .brain.q_learner_CT import QLearner
from .brain.COMA_learner import COMALearner
from .brain.epsilon_schedules import DecayThenFlatSchedule
from util.signal import Signal
from util.logs import Log
import logging


class Agent_CT:
    """
    centralized train
    """

    def __init__(self, param_set, env_info, test_only=False):
        self.n_action = env_info["n_actions"]
        self.n_agent = env_info["n_agents"]
        self.test_only = test_only

        self.log = logging.getLogger('StarCraftII')

        # self.exp_buffer = deque()

        self.memory = Leader_Memmory(env_info)

        if test_only:
            self.policy = self.greedy_policy
        else:
            self.policy = self.epsi_greedy_policy
        self.before_learn = param_set['before_learn']
        self.batch_size = param_set['batch_size']

        ALG = param_set['algorithm']

        if ALG == 'iql_CT':
            self.learner = QLearner(param_set, env_info)
        elif ALG == 'COMA':
            self.learner = COMALearner(param_set, env_info)

        self.schedule = DecayThenFlatSchedule(start=param_set['epsilon_start'], finish=param_set['epsilon_end'],
                                              time_length=param_set['eps'], decay="linear")

    def start_test_mode(self):
        self.test_only = True
        self.policy = self.greedy_policy

    def end_test_mode(self):
        self.test_only = False
        self.policy = self.epsi_greedy_policy


    # 1.0 define policies
    def random_policy(self, avail, t_env=0):
        prop = np.ones(self.n_action) / (np.nonzero(avail)[0].__len__())
        a = np.array(avail)
        action = np.random.choice(np.arange(self.n_action), p=prop * a)
        return action

    def epsi_greedy_policy(self, avail, t_env=0):
        epsilon = self.schedule.eval(t_env)
        q = self.learner.approximate_Q(self.memory.get_current_trajectory()).clone()
        avail = th.FloatTensor(avail)
        q[avail == 0.0] = -float("inf")

        random_numbers = th.rand(self.n_agent)
        pick_random = (random_numbers < epsilon).long()
        random_actions = Categorical(avail.float()).sample().long()
        picked_actions = pick_random * random_actions + (1 - pick_random) * q.argmax(dim=1)
        return picked_actions

    def greedy_policy(self, avail, t_env=0):
        q = self.learner.approximate_Q(self.memory.get_current_trajectory()).clone()
        avail = th.FloatTensor(avail)
        q[avail == 0.0] = -float("inf")
        picked_actions = q.argmax(dim=1)
        return picked_actions

    # 1. improve policy: update_policy
    def update_policy(self):
        message = '\tagents update his target'
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)

        if self.policy == self.random_policy:
            message = "change policy to greedy"
            self.log.info(message)
            Signal.get_signal().emit_signal_str(message)
            self.policy = self.greedy_policy
            return

    # 2. choose action aondition on its policy: select_action
    def select_action(self, experience, t_env=0):
        self.memory.append(experience)
        return self.policy(avail=experience['available_action'], t_env=t_env)

    # 3. learn from experience:  learn
    def learn(self, experience, t_env=0, terminal=False):
        if terminal:
            self.memory.end_trajectory(experience)

            if not self.test_only:
                if self.before_learn > 0:
                    self.before_learn -= 1
                    return

                self.learner.train(self.memory.get_sample(batch_size=self.batch_size), t_env=t_env)


            return
        self.memory.append(experience)


    def save(self, path):
        self.learner.save_model(path)

    def load(self, path):
        self.learner.load_model(path)

    def show_memory(self):
        return self.memory.show_memory()






