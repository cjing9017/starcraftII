from smac.env import StarCraft2Env
import numpy as np
import time
import os

from algorithms.args.leader_CT import Leader
from util.logs import Log
import logging
from util.signal import Signal
from .args.leader_CT import Leader


class MARL(object):

    def __init__(self):
        super(IQL, self).__init__()
        self.log = logging.getLogger('StarCraftII')

    def test(self, env, path, runner, best_score=0):
        self.log.info('start test')
        Signal.get_signal().emit_signal_str('start test')
        super(MARL, self).__init__()

    def test(self, env, path, runner, test_only=False,  best_score=0):
        print("start test")
        runner.start_test()
        new_path = path + 'best_'
        if test_only:
            n_episodes = 100
        else:
            n_episodes = 10
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

            message = "Total reward in episode {} = {}".format(e, episode_reward)
            self.log.info(message)
            Signal.get_signal().emit_signal_str(message)
            print("Total reward in test episode {} = {}".format(e, episode_reward))
            scores.append(episode_reward)
        avg_score = sum(scores) / n_episodes
        if test_only:
            print('average score ', avg_score)
            return
        if avg_score > best_score:
            runner.save(new_path)
        runner.end_test()
        return max(best_score, avg_score)

    def algorithm(self, param_set):
        map_name = param_set['map_name']
        difficulty = param_set['difficulty']
        path = param_set['path']

        env = StarCraft2Env(map_name=map_name, difficulty=difficulty, obs_own_health=True, obs_all_health=True,
                            move_amount=2, continuing_episode=False, obs_pathing_grid=False, obs_terrain_height=False,
                            reward_death_value=10, reward_defeat=0, reward_negative_scale=0.5,
                            reward_scale=True, reward_scale_rate=20, reward_sparse=False, reward_win=200,
                            state_last_action=True, step_mul=8,
                            window_size_x=1418, window_size_y=890)
        env_info = env.get_env_info()
        # {'state_shape': 168,
        #  'obs_shape': 80,
        #  'n_actions': 14,
        #  'n_agents': 8,
        #  'episode_limit': 120}
        message = "env_info: {}".format(env_info)
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)

        n_actions = env_info["n_actions"]
        n_agents = env_info["n_agents"]
        obs_shape = env_info['obs_shape']
        max_seq_len = env_info["episode_limit"]
        n_episodes = 10001
        print("env_info: ",env_info)
        runner = Leader(param_set, env_info=env_info, test_only=False)

        n_episodes = 100000
        t_env = 0
        scores = []
        best_score = 0

        if not os.path.exists(path):
            os.makedirs(path)
        if param_set['load_model']:
            runner.load(path)

        if param_set['test']:
            self.test(env=env, runner=runner, path=path, test_only=True)
            return

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
                runner.learn(joint_action=joint_action, reward=reward, t_env=t_env)

                episode_reward += reward

                if terminated :
                    obs = env.get_obs()
                    state = env.get_state()
                    available_actions = env.get_avail_actions()

                    runner.terminal(observations=obs, state=state, available_actions=available_actions)

            message = "Total reward in episode {} = {}".format(e, episode_reward)
            self.log.info(message)
            Signal.get_signal().emit_signal_str(message)
            print("Total reward in train episode {} = {}".format(e, episode_reward))
            t_env += step
            scores.append(episode_reward)

            if ((e+1) % 500) == 0:
                runner.save(path)
                np.save(path + 'score', scores)
                best_score = self.test(env=env, runner=runner, path=path, best_score=best_score)



        # runner.show_memory()
        runner.save(path)
        np.save(path + 'score', scores)
        env.close()


if __name__ == '__main__':
    map_name = '3m'
    difficulty = '3'
    path = 'model/' + map_name + '_COMA_3/'

    # COMA set
    param_set = {}
    param_set['algorithm'] = 'COMA'
    param_set['gamma'] = 0.99
    param_set['td_lambda'] = 0.8
    param_set['learning_rate'] = 0.0005
    param_set['alpha'] = 0.99
    param_set['eps'] = 1e-05
    param_set['epsilon_start'] = 1
    param_set['epsilon_end'] = 0.01
    param_set['time_length'] = 100000
    param_set['grad_norm_clip'] = 10
    # param_set['before_learn'] = 10
    # param_set['batch_size'] = 8
    param_set['before_learn'] = 50
    param_set['batch_size'] = 16
    param_set['target_update_interval'] = 400
    param_set['load_model'] = True
    param_set['test'] = True

    # # iql set
    param_set['algorithm'] = 'iql_CT'
    param_set['load_model'] = True
    param_set['test'] = True

    path = 'model/' + map_name + '_iql_CT_3/'

    param_set['map_name'] = map_name
    param_set['difficulty'] = difficulty
    param_set['path'] = path


    thread = MARL()
    thread.algorithm(param_set)