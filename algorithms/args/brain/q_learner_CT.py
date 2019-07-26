import copy
import torch as th
from torch.optim import RMSprop
import numpy as np
import os

from .rnn_agent import RNNAgent

class QLearner:
    """
    1. DQN- RNNAgent
    2. train
    """
    def __init__(self, n_agent, n_action, obs_shape=80):
        self.n_agent = n_agent
        self.n_action = n_action
        self.obs_shape = obs_shape

        self.gamma = 0.99
        self.learning_rate = 0.0005
        self.alpha = 0.99
        self.eps = 1e-05

        self.obs_last_action = True
        self.obs_agent_id = True
        output_shape = n_action
        input_shape = self._get_input_shape()

        self.Q = RNNAgent(input_shape,output_shape)
        self.params = self.Q.parameters()
        self.target_Q = copy.deepcopy(self.Q)
        self.optimiser = RMSprop(params=self.params, lr=self.learning_rate, alpha=self.alpha, eps=self.eps)

        self.hidden_states = None

    def update(self):
        self.target_Q.load_state_dict(self.Q.state_dict())

    def approximate_Q(self, batch):
        self.init_hidden(batch['batch_size'], self.Q)
        for t in range(batch['len']):
            outs = self.forward(batch, t, Q_func=self.Q)
        return outs

    def train(self, batch):
        reward = batch["reward"]
        action = batch["action"]
        done = batch["done"]
        avail_actions = batch["available_action"]
        batch_size = batch['batch_size']
        mask = batch['mask']

        action = action.transpose(1, 2).reshape(batch_size * self.n_agent, -1).unsqueeze(2)
        avail_actions = avail_actions[:, 1:].transpose(1, 2).reshape(batch_size * self.n_agent, -1, self.n_action)
        done = done.reshape(batch_size * self.n_agent, -1)
        mask = mask.reshape(batch_size * self.n_agent, -1)
        reward = reward.reshape(batch_size * self.n_agent, -1)

        self.init_hidden(batch_size, self.Q)
        out_batch = []
        for t in range(batch['len']):
            outs = self.forward(batch, t, Q_func=self.Q)
            out_batch.append(outs)
        out_batch = th.stack(out_batch, dim=1)
        chosen_action_qvals = th.gather(out_batch[:, :-1], dim=2, index=action).squeeze(2)

        self.init_hidden(batch_size, self.target_Q)
        target_out_batch = []
        for t in range(batch['len']):
            outs = self.forward(batch, t, Q_func=self.target_Q)
            target_out_batch.append(outs)
        target_out_batch = th.stack(target_out_batch[1:], dim=1)  # Concat across time
        target_out_batch[avail_actions == 0] = -9999999
        # Max over target Q-Values if self.args.double_q:
        if False:
            # Get actions that maximise live Q (for double q-learning)
            mac_out[avail_actions == 0] = -9999999
            cur_max_actions = mac_out[:, 1:].max(dim=3, keepdim=True)[1]
            target_max_qvals = th.gather(target_mac_out, 3, cur_max_actions).squeeze(3)
        else:
            # 为什么要取[0]
            target_max_qvals = target_out_batch.max(dim=2)
            target_max_qvals = target_max_qvals[0]

        # Calculate 1-step Q-Learning targets
        # print('reward.shape', reward.shape)
        # print('target_max_qvals.shape', target_max_qvals.shape)
        # print(done.shape)
        targets = reward + self.gamma * (1 - done) * target_max_qvals
        td_error = (chosen_action_qvals - targets.detach()) * mask
        loss = (td_error ** 2).sum() / mask.sum()

        # Optimise
        self.optimiser.zero_grad()
        loss.backward()
        grad_norm = th.nn.utils.clip_grad_norm_(self.params, 10)
        self.optimiser.step()


    def forward(self, batch, t, Q_func):
        inputs = self._build_input(batch, t)
        outs, self.hidden_states = Q_func(inputs, self.hidden_states)
        return outs


    def _build_input(self, batch, t):
        batch_size = batch['batch_size']
        inputs = []
        inputs.append(batch["observation"][:, t])  # b1av
        if self.obs_last_action:
            if t == 0:
                inputs.append(th.zeros((batch_size, self.n_agent,self.n_action)))
            else:
                inputs.append(batch["action_onehot"][:, t - 1])
        if self.obs_agent_id:
            inputs.append(th.eye(self.n_agent).unsqueeze(0).expand(batch_size, -1, -1))
        inputs = th.cat([x.reshape(batch_size * self.n_agent, -1) for x in inputs], dim=1)
        return inputs

    def _get_input_shape(self):
        input_shape = self.obs_shape
        if self.obs_last_action:
            input_shape += self.n_action
        if self.obs_agent_id:
            input_shape += self.n_agent

        return input_shape

    def init_hidden(self, batch_size, Q_func):
        self.hidden_states = Q_func.init_hidden().unsqueeze(0).expand(batch_size,self.n_agent, -1)  # bav

    def save_model(self, path):
        th.save(self.Q.state_dict(), path + 'Q' +'.pt')

    def load_model(self, path):
        file = path + 'best_Q' + '.pt'
        if os.path.isfile(file):
            self.Q.load_state_dict(th.load(file))
        else:
            file = path + 'Q' + '.pt'
            if os.path.isfile(file):
                self.Q.load_state_dict(th.load(file))
            else:
                print("here have not such model")
        self.target_Q.load_state_dict(self.Q.state_dict())
        return


