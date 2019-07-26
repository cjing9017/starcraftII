import numpy as np
import random as rd
import torch as th
from torch.distributions import Categorical

from .brain.mamory import Leader_Memmory
from .brain.q_learner_CT import QLearner
from .brain.epsilon_schedules import DecayThenFlatSchedule

class Agent_CT:
    """
    centralized train
    """
    def __init__(self, n_agents, n_actions, max_seq_len, obs_shape, test_only=False):
        self.n_agents = n_agents
        self.n_actions = n_actions
        self.test_only = test_only

        # self.exp_buffer = deque()

        self.memory = Leader_Memmory(n_action=n_actions, n_agent=n_agents, max_seq_len=max_seq_len, obs_shape=obs_shape)

        if test_only:
            self.policy = self.greedy_policy
        else:
            self.policy = self.epsi_greedy_policy
        self.policy_update_frequncy = 200
        self.clock = 0
        self.before_learn = 32

        self.learner = QLearner(n_agent=self.n_agents, n_action=self.n_actions, obs_shape=obs_shape)
        self.learn_frequncy = 10

        self.schedule = DecayThenFlatSchedule(start=1.0, finish=0.05, time_length=50000, decay="linear")

    def start_test_mode(self):
        self.test_only = True
        self.policy = self.greedy_policy

    def end_test_mode(self):
        self.test_only = False
        self.policy = self.epsi_greedy_policy


    # 1.0 define policies
    def random_policy(self, avail, t_env=0):
        prop = np.ones(self.n_actions) / (np.nonzero(avail)[0].__len__())
        a = np.array(avail)
        action = np.random.choice(np.arange(self.n_actions), p=prop * a)
        return action

    def epsi_greedy_policy(self, avail, t_env=0):
        epsilon = self.schedule.eval(t_env)
        q = self.learner.approximate_Q(self.memory.get_current_trajectory()).clone()
        avail = th.FloatTensor(avail)
        q[avail == 0.0] = -float("inf")

        random_numbers = th.rand(self.n_agents)
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
        print('\tagents update his target')
        if self.policy == self.random_policy:
            print("change policy to greedy")
            self.policy = self.greedy_policy
            return
        self.learner.update()

    # 2. choose action aondition on its policy: select_action
    def select_action(self, experience, t_env=0):
        self.memory.append(experience)
        return self.policy(avail=experience['available_action'], t_env=t_env)

    # 3. learn from experience:  learn
    def learn(self, experience, terminal=False):
        if terminal:
            self.clock += 1
            self.memory.end_trajectory(experience)

            if not self.test_only:
                if self.before_learn > 0:
                    self.before_learn -= 1
                    return

                self.learner.train(self.memory.get_sample(batch_size=32))

                if self.clock % self.policy_update_frequncy == 0:
                    self.update_policy()
                    self.clock = 0

            return
        self.memory.append(experience)


    def save(self, path):
        self.learner.save_model(path)

    def load(self, path):
        self.learner.load_model(path)

    def show_memory(self):
        return self.memory.show_memory()






