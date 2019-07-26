from smac.env import StarCraft2Env
import numpy as np
import time
import os

from algorithms.args.leader_CT import Leader

class IQL(object):
    def __init__(self):
        super(IQL, self).__init__()

    def test(self, env, path, runner, best_score=0):
        print("start test")
        runner.start_test()
        new_path = path + 'best_'
        test_only = True
        n_episodes = 20
        scores = []
        for e in range(n_episodes):
            # print("eps ", e)

            env.reset()
            terminated = False
            episode_reward = 0
            step = 0
            while not terminated:
                if test_only:
                    time.sleep(0.2)

                step += 1

                obs = env.get_obs()
                state = env.get_state()
                available_actions = env.get_avail_actions()
                joint_action = runner.select_actions(observations=obs, state=state, available_actions=available_actions)

                reward, terminated, _ = env.step(joint_action)
                runner.learn(joint_action=joint_action, reward=reward)

                episode_reward += reward

                if terminated :
                    obs = env.get_obs()
                    state = env.get_state()
                    available_actions = env.get_avail_actions()

                    runner.terminal(observations=obs, state=state, available_actions=available_actions)

            print("Total reward in episode {} = {}".format(e, episode_reward))
            scores.append(episode_reward)
        avg_score = sum(scores) / n_episodes
        if avg_score > best_score:
            runner.save(new_path)
        runner.end_test()
        return max(best_score, avg_score)

    def algorithm(self, map_name='3m', difficulty='3',path='../model/3m_iql_CT_3/', load_model=True,
                  window_size_x=1418, window_size_y=890, window_loc=(5, 155)):
        difficulty = difficulty
        if load_model== True:
            path = path
        else:
            path = 'model/' + map_name + '_iql/'

        env = StarCraft2Env(map_name=map_name, difficulty=difficulty, obs_own_health=True, obs_all_health=True,
                            move_amount=2, continuing_episode=False, obs_pathing_grid=False, obs_terrain_height=False,
                            reward_death_value=10, reward_defeat=0, reward_negative_scale=0.5,
                            reward_scale=True, reward_scale_rate=20, reward_sparse=False, reward_win=200,
                            state_last_action=True, step_mul=8,
                            window_size_x=window_size_x, window_size_y=window_size_y)
        env_info = env.get_env_info()
        # {'state_shape': 168,
        #  'obs_shape': 80,
        #  'n_actions': 14,
        #  'n_agents': 8,
        #  'episode_limit': 120}
        print("env_info: ",env_info)

        n_actions = env_info["n_actions"]
        n_agents = env_info["n_agents"]
        obs_shape = env_info['obs_shape']
        max_seq_len = env_info["episode_limit"]
        n_episodes = 10001
        t_env = 0
        scores = []
        best_score = 0

        runner = Leader(n_agents=n_agents, n_actions=n_actions, max_seq_len= max_seq_len, obs_shape=obs_shape, test_only=False)

        if not os.path.exists(path):
            os.makedirs(path)
        if load_model:
            runner.load(path)

        for e in range(n_episodes):
            # print("eps ", e)

            env.reset()
            terminated = False
            episode_reward = 0
            step = 0
            while not terminated:

                step += 1

                obs = env.get_obs()
                state = env.get_state()
                available_actions = env.get_avail_actions()
                joint_action = runner.select_actions(observations=obs, state=state, available_actions=available_actions, t_env=t_env)

                reward, terminated, _ = env.step(joint_action)
                runner.learn(joint_action=joint_action, reward=reward)

                episode_reward += reward

                if terminated :
                    obs = env.get_obs()
                    state = env.get_state()
                    available_actions = env.get_avail_actions()

                    runner.terminal(observations=obs, state=state, available_actions=available_actions)

            print("Total reward in episode {} = {}".format(e, episode_reward))
            t_env += step
            scores.append(episode_reward)

            if (e % 1000)==0:
                runner.save(path)
                np.save(path + 'score', scores)

            if (e % 500) == 0:
                best_score = self.test(env=env, runner=runner, path=path, best_score=best_score)



        # runner.show_memory()
        runner.save(path)
        np.save(path + 'score', scores)
        env.close()

if __name__ == '__main__':
    map_name = '3m'
    difficulty = '3'
    path = 'model/' + map_name + '_iql_CT_3/'
    thread = IQL()
    thread.algorithm(map_name=map_name, difficulty=difficulty,path=path, load_model=True)