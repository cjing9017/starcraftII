from .agent_CT import Agent_CT


class Leader:
    def __init__(self, n_agents, n_actions, max_seq_len, obs_shape, test_only):
        self.test_only = test_only

        self.n_agents = n_agents
        self.n_actions = n_actions
        self.workers = Agent_CT(n_agents=n_agents, n_actions=n_actions, max_seq_len=max_seq_len, obs_shape=obs_shape, test_only=test_only)
        self.clock = 0
        self.episode_reward = 0

    def select_actions(self, observations, state, available_actions, t_env=0):
        exprience = {
            "observation": observations,
            "state": state,
            "available_action": available_actions,
        }
        joint_action = self.workers.select_action(exprience, t_env)
        return joint_action

    def learn(self, joint_action, reward):
        self.episode_reward += reward
        exprience = {
            "joint_action": joint_action,
            "reward": reward
        }
        self.workers.learn(exprience)

    def terminal(self, observations, state, available_actions):
        exprience = {
            "observation": observations,
            "available_action": available_actions,
            "state": state,
            "eps_reward": self.episode_reward

        }
        self.workers.learn(exprience, terminal=True)
        self.episode_reward = 0

    def save(self, path):
        self.workers.save(path)

    def load(self, path):
        self.workers.load(path)

    def show_memory(self):
        self.workers[0].show_memory()

    def start_test(self):
        self.workers.start_test_mode()

    def end_test(self):
        self.workers.end_test_mode()
