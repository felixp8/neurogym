#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:22:19 2019

@author: linux
"""
# TODO: allow tasks parameters to be modfied
import gym
from neurogym.wrappers import trial_hist
from neurogym.wrappers import manage_data
from neurogym.wrappers import combine
from neurogym.wrappers import reaction_time
from neurogym.wrappers import pass_reward
from neurogym.wrappers import pass_action


def build_env(env_id, inst=0, **all_args):
    """
    builds environment with specifications indicated in args
    """
    env_keys = ['dt']
    if env_id == 'RDM-v0':
        env_keys.append('timing')
        env_keys.append('stimEv')
    env_args = {x: all_args[x] for x in env_keys}
    # TODO: allow for envs to be wrapped before combined
    if all_args['combine']:
        env1 = gym.make(env_id, **env_args)
        env2 = gym.make(all_args['env2'], **env_args)
        env = combine.combine(env1, env2)
    else:
        env = gym.make(env_id, **env_args)
        if all_args['trial_hist']:
            env = trial_hist.TrialHistory(env, rep_prob=all_args['rep_prob'],
                                          block_dur=all_args['bl_dur'])
        if all_args['reaction_time']:
            env = reaction_time.ReactionTime(env)
        if all_args['pass_reward']:
            env = pass_reward.PassReward(env)
        if all_args['pass_action']:
            env = pass_action.PassAction(env)
    env = manage_data.manage_data(env, inst=inst, plt_tr=all_args['figs'],
                                  folder=all_args['save_path'])
    return env
