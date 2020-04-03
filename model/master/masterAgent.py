from model.master.runner import Runner
from smac.env import StarCraft2Env
from model.master.common.arguments import get_common_args, get_coma_args, get_mixer_args, get_commnet_args

from PyQt5.QtCore import QThread
from resource import globalInformation
from resource import strings
from util.signal import Signal


class MasterAgent(QThread):

    def __int__(self, map_name, alg_name, epoch):
        super(MasterAgent, self).__int__()

    def run(self):
        self.log = logging.getLogger('StarCraftII')
        for i in range(8):
            args = get_common_args()
            map_name = globalInformation.get_value(strings.TYPE_MAP)
            alg_name = globalInformation.get_value(strings.TYPE_POLICY)
            if map_name is not None:
                args.map = map_name
            if alg_name is not None:
                args.alg = alg_name
            args.evaluate_epoch = 100
            if args.alg == 'coma':
                args = get_coma_args(args)
            elif args.alg == 'commnet_coma':
                args = get_commnet_args(args)
            else:
                args = get_mixer_args(args)
            env = StarCraft2Env(map_name=args.map,
                                step_mul=args.step_mul,
                                difficulty=args.difficulty,
                                game_version=args.game_version,
                                replay_dir=args.replay_dir,
                                window_size_x=1418,
                                window_size_y=890,
                                window_loc=(5, 155)
                                )
            env_info = env.get_env_info()
            args.n_actions = env_info["n_actions"]
            args.n_agents = env_info["n_agents"]
            args.state_shape = env_info["state_shape"]
            args.obs_shape = env_info["obs_shape"]
            args.episode_limit = env_info["episode_limit"]
            runner = Runner(env, args)
            if args.learn:
                runner.run(i)
            else:
                win_rate = runner.evaluate_sparse()
                message = 'The win rate of {} is  {}'.format(args.alg, win_rate)
                self.log.info(message)
                Signal.get_signal().emit_signal_str(message)
                break
            env.close()


if __name__ == '__main__':
    thread = MasterAgent()
    thread.start()
