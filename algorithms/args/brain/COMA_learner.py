import copy
import torch as th
from torch.optim import RMSprop
import numpy as np
import os

from .rnn_agent import RNNAgent
from .COMA_critic import COMACritic

def build_td_lambda_targets(rewards, terminated, mask, target_qs, n_agents, gamma, td_lambda):
    # Assumes  <target_qs > in B*T*A and <reward >, <terminated >, <mask > in (at least) B*T-1*1
    # Initialise  last  lambda -return  for  not  terminated  episodes
    ret = target_qs.new_zeros(*target_qs.shape)
    # print("ret.shaoe: ", ret.shape)
    # print('ter.shape', terminated.shape, th.sum(terminated, dim=1).shape)
    terminated = terminated.transpose(1, 2)
    mask = mask.transpose(1, 2)
    rewards = rewards.transpose(1, 2)

    ret[:, -1] = target_qs[:, -1] * (1 - th.sum(terminated, dim=1))
    # Backwards  recursive  update  of the "forward  view"
    for t in range(ret.shape[1] - 2, -1,  -1):
        ret[:, t] = td_lambda * gamma * ret[:, t + 1] + mask[:, t] \
                    * (rewards[:, t] + (1 - td_lambda) * gamma * target_qs[:, t + 1] * (1 - terminated[:, t]))
    # Returns lambda-return from t=0 to t=T-1, i.e. in B*T-1*A
    return ret


class COMALearner:
    def __init__(self, param_set, env_info):
        self.n_action = env_info["n_actions"]
        self.n_agent = env_info["n_agents"]
        self.obs_shape = env_info['obs_shape']

        self.gamma = param_set['gamma']
        self.td_lambda = param_set['td_lambda']
        self.learning_rate = param_set['learning_rate']
        self.alpha = param_set['alpha']
        self.eps = param_set['eps']
        self.grad_norm_clip = param_set['grad_norm_clip']

        self.obs_last_action = True
        self.obs_agent_id = True
        output_shape = self.n_action
        input_shape = self._get_Q_input_shape()

        self.Q = RNNAgent(input_shape,output_shape)
        self.critic = COMACritic(env_info)
        self.target_critic = copy.deepcopy(self.critic)

        self.agent_params = list(self.Q.parameters())
        self.critic_params = list(self.critic.parameters())
        self.params = self.agent_params + self.critic_params

        self.agent_optimiser = RMSprop(params=self.agent_params, lr=self.learning_rate, alpha=self.alpha, eps=self.eps)
        self.critic_optimiser = RMSprop(params=self.critic_params, lr=self.learning_rate, alpha=self.alpha, eps=self.eps)

        self.critic_training_steps = 0
        self.target_update_interval = param_set['target_update_interval']
        self.last_target_update_step = 0

    def _get_Q_input_shape(self):
        input_shape = self.obs_shape
        if self.obs_last_action:
            input_shape += self.n_action
        if self.obs_agent_id:
            input_shape += self.n_agent

        return input_shape

    def _train_critic(self, batch):
        reward = batch["reward"]
        action = batch["action"]
        done = batch["done"]
        batch_size = batch['batch_size']
        mask = batch['mask']


        # Optimise critic
        target_q_vals = self.target_critic(batch)[:, :-1] #batch:t:agent:action
        # print('target_q_vals.shape:', target_q_vals.shape, action.unsqueeze(3).shape)
        targets_taken = th.gather(target_q_vals, dim=3, index=action.unsqueeze(3)).squeeze(3)

        # Calculate td-lambda targets
        targets = build_td_lambda_targets(reward, done, mask, targets_taken, self.n_agent, self.gamma, self.td_lambda)

        q_vals = th.zeros_like(target_q_vals)

        # print('reward:', reward.shape) # batch:agent:t = mask.shpe
        # print("targets:", targets.shape) # batch:t:agent
        # print('q_vals:', q_vals.shape) #batch:t:agent:action

        for t in reversed(range(reward.size(2))):
            mask_t = mask[:,:, t] # batch:agent:
            if mask_t.sum() == 0:
                continue

            q_t = self.critic(batch, t) # batch:1:agent:action
            q_vals[:, t] = q_t.view(batch_size, self.n_agent, self.n_action)
            # print('q_t.shape ', q_t.shape)
            # print("action.shape ", (action[:, t]).unsqueeze(1).unsqueeze(3).shape)
            q_taken = th.gather(q_t, dim=3, index=(action[:, t]).unsqueeze(1).unsqueeze(3)).squeeze(3).squeeze(1)# batch:agent
            targets_t = targets[:, t] # batch:agent

            td_error = (q_taken - targets_t.detach())

            # 0-out the targets that came from padded data
            masked_td_error = td_error * mask_t

            # Normal L2 loss, take mean over actual data
            loss = (masked_td_error ** 2).sum() / mask_t.sum()
            self.critic_optimiser.zero_grad()
            loss.backward()
            grad_norm = th.nn.utils.clip_grad_norm_(self.critic_params, self.grad_norm_clip)
            self.critic_optimiser.step()
            self.critic_training_steps += 1

        return q_vals

    def _update_critic_targets(self):
        self.target_critic.load_state_dict(self.critic.state_dict())

    def init_Q_hidden(self, batch_size):
        self.hidden_states = self.Q.init_hidden().unsqueeze(0).expand(batch_size,self.n_agent, -1)  # bav

    def _build_input_forQ(self, batch, t):
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

    def Q_forward(self, batch, t):
        inputs = self._build_input_forQ(batch, t)
        outs, self.hidden_states = self.Q(inputs, self.hidden_states)
        return outs

    def train(self, batch, t_env):
        reward = batch["reward"]
        action = batch["action"]
        done = batch["done"]
        avail_action = batch["available_action"]
        batch_size = batch['batch_size']
        mask = batch['mask']

        action = action.transpose(1, 2).reshape(batch_size * self.n_agent, -1).unsqueeze(2)
        avail_action = avail_action[:, 1:].transpose(1, 2).reshape(batch_size * self.n_agent, -1, self.n_action)
        done = done.reshape(batch_size * self.n_agent, -1)
        mask = mask.reshape(batch_size * self.n_agent, -1)
        reward = reward.reshape(batch_size * self.n_agent, -1)


        q_val = self._train_critic(batch)

        self.init_Q_hidden(batch_size)
        out_batch = []
        for t in range(batch['len']-1):
            outs = self.Q_forward(batch, t)
            out_batch.append(outs)
        out_batch = th.stack(out_batch, dim=1)
        out_batch[avail_action == 0] = 0
        out_batch = out_batch / out_batch.sum(dim=-1, keepdim=True)
        out_batch[avail_action == 0] = 0

        # chosen_action_qvals = th.gather(out_batch[:, :-1], dim=2, index=action).squeeze(2)
        # print('q_val:',q_val.shape) # batch:t:agent:action
        # print('out_batch',out_batch.shape) # batch * agent: t: action
        # print('action:', action.shape) # #batch * agent :t:1
        # print('mask', mask.shape) # #batch * agent :t
        # Calculated baseline
        q_val = q_val.transpose(1,2).reshape(-1, self.n_action)
        pi = out_batch.view(-1, self.n_action)
        baseline = (pi * q_val).sum(-1).detach()

        # Calculate policy grad with mask
        q_taken = th.gather(q_val, dim=1, index=action.reshape(-1, 1)).squeeze(1)
        pi_taken = th.gather(pi, dim=1, index=action.reshape(-1, 1)).squeeze(1)
        mask = mask.view(-1)
        pi_taken[mask== 0] = 1.0
        log_pi_taken = th.log(pi_taken)

        advantages = (q_taken - baseline).detach()

        coma_loss = - ((advantages * log_pi_taken) * mask).sum() / mask.sum()

        # Optimise agents
        self.agent_optimiser.zero_grad()
        coma_loss.backward()
        grad_norm = th.nn.utils.clip_grad_norm_(self.agent_params, self.grad_norm_clip)
        self.agent_optimiser.step()

        if (self.critic_training_steps - self.last_target_update_step) / self.target_update_interval >= 1.0:
            print('Critic updated')
            self._update_critic_targets()
            self.last_target_update_step = self.critic_training_steps

    def approximate_Q(self, batch):
        self.init_Q_hidden(batch['batch_size'])
        for t in range(batch['len']):
            outs = self.Q_forward(batch, t)
        return outs

    def save_model(self, path):
        th.save(self.Q.state_dict(), path + 'Q' +'.pt')
        th.save(self.critic.state_dict(), "{}critic.th".format(path))
        th.save(self.agent_optimiser.state_dict(), "{}agent_opt.th".format(path))
        th.save(self.critic_optimiser.state_dict(), "{}critic_opt.th".format(path))

    def load_model(self, path):
        file = path + 'load_Q.pt'
        file_c = path + 'load_critic.th'
        file_aopt = path + 'load_agent_opt.th'
        file_copt = path + 'load_critic_opt.th'
        if not os.path.isfile(file):
            file = path + 'best_Q.pt'
            file_c = path + 'best_critic.th'
            file_aopt = path + 'best_agent_opt.th'
            file_copt = path + 'best_critic_opt.th'
            if not os.path.isfile(file):
                file = path + 'Q.pt'
                file_c = path + 'critic.th'
                file_aopt = path + 'agent_opt.th'
                file_copt = path + 'critic_opt.th'
                if not os.path.isfile(file):
                    print("here have not such model")
                    return
        self.Q.load_state_dict(th.load(file))
        self.critic.load_state_dict(th.load(file_c))
        self.target_critic.load_state_dict(self.critic.state_dict())
        self.agent_optimiser.load_state_dict(th.load(file_aopt))
        self.critic_optimiser.load_state_dict(th.load(file_copt))

        print('sucess load the model in ',file)
        return



