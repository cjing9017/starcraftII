import torch as th
import torch.nn as nn
import torch.nn.functional as F


class COMACritic(nn.Module):
    def __init__(self, env_info):
        super(COMACritic, self).__init__()

        self.n_action = env_info["n_actions"]
        self.n_agent = env_info["n_agents"]
        self.obs_shape = env_info['obs_shape']
        self.state_shape = env_info['state_shape']


        input_shape = self._get_input_shape(self.state_shape, self.obs_shape)
        self.output_type = "q"

        # Set up network layers
        self.fc1 = nn.Linear(input_shape, 128)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, self.n_action)

    def forward(self, batch, t=None):
        inputs = self._build_inputs(batch, t=t)
        x = F.relu(self.fc1(inputs))
        x = F.relu(self.fc2(x))
        # x = self.dropout(x)
        q = self.fc3(x)
        return q

    def _build_inputs(self, batch, t=None):
        bs = batch['batch_size']
        max_t = batch['len'] if t is None else 1
        ts = slice(None) if t is None else slice(t, t+1)
        inputs = []
        # state
        state = batch["state"].transpose(1,2)
        # print("state: ",state[:, ts].shape)
        inputs.append(state[:, ts])

        # observation
        # print("obs: ", batch["observation"][:, ts].shape)
        inputs.append(batch["observation"][:, ts])

        # actions (masked out by agent)
        actions = th.cat([batch["action_onehot"], th.zeros_like(batch["action_onehot"][:, 0:1])], dim=1)
        # print('act:', actions.shape)
        # print('maxt:', max_t)
        actions = actions[:, ts].view(bs, max_t , 1, -1).repeat(1, 1, self.n_agent, 1)
        agent_mask = (1 - th.eye(self.n_agent))
        agent_mask = agent_mask.view(-1, 1).repeat(1, self.n_action).view(self.n_agent, -1)
        # print("actions: ", (actions * agent_mask.unsqueeze(0).unsqueeze(0)).shape )
        inputs.append(actions * agent_mask.unsqueeze(0).unsqueeze(0))

        # last actions
        if t == 0:
            # print("t=0, last: ", th.zeros_like(batch["action_onehot"][:, 0:1]).view(bs, max_t, 1, -1).repeat(1, 1, self.n_agent, 1).shape )
            inputs.append(th.zeros_like(batch["action_onehot"][:, 0:1]).view(bs, max_t, 1, -1).repeat(1, 1, self.n_agent, 1))
        elif isinstance(t, int):
            # print("t != 0 last: ", batch["action_onehot"][:, slice(t-1, t)].view(bs, max_t, 1, -1).repeat(1, 1, self.n_agent, 1).shape)
            inputs.append(batch["action_onehot"][:, slice(t-1, t)].view(bs, max_t, 1, -1).repeat(1, 1, self.n_agent, 1))
        else:
            last_actions = th.cat([th.zeros_like(batch["action_onehot"][:, 0:1]), batch["action_onehot"]], dim=1)
            last_actions = last_actions.view(bs, max_t, 1, -1).repeat(1, 1, self.n_agent, 1)
            # print("all last: ", last_actions.shape)
            inputs.append(last_actions)

        # print('agent: ', th.eye(self.n_agent).unsqueeze(0).unsqueeze(0).expand(bs, max_t, -1, -1).shape)

        inputs.append(th.eye(self.n_agent).unsqueeze(0).unsqueeze(0).expand(bs, max_t, -1, -1))

        inputs = th.cat([x.reshape(bs, max_t, self.n_agent, -1) for x in inputs], dim=-1)
        # print('input:',inputs.shape)
        return inputs

    def _get_input_shape(self, state_shape, obs_shape):
        # state
        input_shape = state_shape
        # observation
        input_shape += obs_shape
        # actions and last actions
        input_shape += self.n_action * self.n_agent * 2
        # agent id
        input_shape += self.n_agent
        return input_shape