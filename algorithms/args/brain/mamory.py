import numpy as np
import torch as th
import random as rd
import copy
from queue import PriorityQueue
from collections import deque

class Leader_Memmory:
    """
    unimplement!!!
    1. append(exprience):
    2. get_sample
    """

    def __init__(self, env_info):
        self.n_action = env_info["n_actions"]
        self.n_agent = env_info["n_agents"]
        self.obs_shape = env_info['obs_shape']
        self.max_seq_len = env_info['episode_limit']
        self.state_shape = env_info['state_shape']

        self.PQ = False
        if self.PQ:
            self.trajectories = PriorityQueue()
        else:
            self.trajectories = deque()
        self.max_n_trajextories = 500
        self.max_score = 0
        self.episode_index = 0

        self.current_trajectory = {
            'observation': [],
            'state': [],
            'available_action': [],
            'joint_action': [],
            'action_onehot': [],
            'reward': [],
            'score': 0
        }

        self.preprocess = {
            'joint_action': {
                'action_onehot': self.action_onehot
            }
        }

    def action_onehot(self, joint_action):
        one_hot = th.zeros((self.n_agent, self.n_action))
        # print(joint_action.unsqueeze(1))
        one_hot = one_hot.scatter(dim=1, index=joint_action.unsqueeze(1), source=1)
        # one_hot = one_hot.scatter(dim=1, index=joint_action.unsqueeze(1), value=1)
        # print(one_hot)
        return one_hot

    def append(self, exprience):
        for key in exprience:
            if key in self.current_trajectory:
                self.current_trajectory[key].append(exprience[key])
            if key in self.preprocess:
                for new_key in self.preprocess[key]:
                    preprocesser = self.preprocess[key][new_key]
                    self.current_trajectory[new_key].append(preprocesser(exprience[key]))

    def end_trajectory(self, exprience):
        self.append(exprience)
        self.current_trajectory['score'] = exprience['eps_reward']

        if self.PQ:
            self.trajectories.put((exprience['eps_reward'], self.episode_index, copy.deepcopy(self.current_trajectory)))
        else:
            self.trajectories.append(copy.deepcopy(self.current_trajectory))
        self.episode_index += 1
        self.current_trajectory.clear()

        self.current_trajectory = {
            'observation': [],
            'state': [],
            'available_action': [],
            'joint_action': [],
            'action_onehot': [],
            'reward': [],
            'score': 0
        }
        self.max_score = max(self.max_score, exprience['eps_reward'])
        if self.PQ:
            if self.trajectories.queue.__len__() > self.max_n_trajextories:
                self.trajectories.get()
        else:
            if self.trajectories.__len__() > self.max_n_trajextories:
                self.trajectories.popleft()

    def get_item(self, e):
        if self.PQ:
            _, _, trajectory = self.trajectories.queue[e]
        else:
            trajectory = self.trajectories[e]
        trajectory_len = len(trajectory['observation'])
        fill_len = self.max_seq_len + 1 - trajectory_len
        mask = th.zeros(self.max_seq_len)
        mask[:trajectory_len-1] = 1
        mask = mask.expand(self.n_agent, -1)
        done = th.zeros(self.max_seq_len)
        done[trajectory_len-2:] = 1
        done = done.expand(self.n_agent, -1)
        observation = th.FloatTensor(trajectory['observation'])
        observation = th.cat((observation, th.zeros((fill_len,self.n_agent, self.obs_shape))))
        reward = th.FloatTensor(trajectory['reward'])
        reward = th.cat((reward, th.zeros(fill_len))).expand(self.n_agent, -1)
        action = th.stack(trajectory['joint_action'])
        action = th.cat((action, th.zeros((fill_len, self.n_agent), dtype=th.long)))
        action_onehot = th.stack(trajectory['action_onehot'])
        action_onehot = th.cat((action_onehot, th.zeros((fill_len, self.n_agent, self.n_action))))
        action_avail = th.FloatTensor(trajectory['available_action'])
        action_avail = th.cat((action_avail, th.zeros((fill_len, self.n_agent, self.n_action))))
        return mask, done, observation, reward, action, action_onehot, action_avail

    def get_sample(self, batch_size=32):
        """
        目前来看 seq_len 都是max，但后面会不会有不同 如果不足就需要补充
        :param batch_size:
        :return:
        """
        obs_batch = []
        avail_batch = []
        act_batch = []
        rew_batch = []
        action_onehot_batch = []
        mask_batch = []
        done_batch = []

        if self.PQ:
            trajectory_len = self.trajectories.queue.__len__()
        else:
            trajectory_len = self.trajectories.__len__()

        samlpe_new_memory = batch_size // 4
        new_memory = trajectory_len // 4

        for i in range(batch_size - samlpe_new_memory):
            e = - rd.randint(1, new_memory)
            mask, done, observation, reward, action, action_onehot, action_avail = self.get_item(e)
            mask_batch.append(mask)
            done_batch.append(done)
            obs_batch.append(observation)
            rew_batch.append(reward)
            act_batch.append(action)
            action_onehot_batch.append(action_onehot)
            avail_batch.append(action_avail)

        for i in range(samlpe_new_memory):
            e = rd.randint(0, trajectory_len - 1)
            mask, done, observation, reward, action, action_onehot, action_avail = self.get_item(e)
            mask_batch.append(mask)
            done_batch.append(done)
            obs_batch.append(observation)
            rew_batch.append(reward)
            act_batch.append(action)
            action_onehot_batch.append(action_onehot)
            avail_batch.append(action_avail)

        batch = {
            'observation': th.stack(obs_batch),
            'available_action': th.stack(avail_batch),
            'action': th.stack(act_batch),
            'action_onehot': th.stack(action_onehot_batch),
            'reward': th.stack(rew_batch),
            'done': th.stack(done_batch),
            'mask': th.stack(mask_batch),
            'len': self.max_seq_len + 1,
            'batch_size': batch_size
        }

        return batch

    def show_memory(self):
        print("agent ", self.index)
        if self.PQ:
            for _, _, t in self.trajectories.queue:
                print("len: ", len(t['observation']), "; score: ", t['score'])

    def get_current_trajectory(self):
        if self.current_trajectory['action_onehot'] == []:
            current_action_onehot = []
        else:
            current_action_onehot = th.stack(self.current_trajectory['action_onehot']).unsqueeze(0)
        batch = {
            'observation': th.FloatTensor([self.current_trajectory['observation']]),
            'action_onehot': current_action_onehot,
            'len': len(self.current_trajectory['observation']),
            'batch_size': 1
        }
        return batch
