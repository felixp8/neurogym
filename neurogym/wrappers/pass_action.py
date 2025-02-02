#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from gym import Wrapper
from gym import spaces


class PassAction(Wrapper):
    """Modifies observation by adding the previous action."""
    metadata = {
        'description': 'Modifies observation by adding the previous action.',
        'paper_link': None,
        'paper_name': None,
    }

    def __init__(self, env, one_hot=False):
        super().__init__(env)
        self.env = env
        # TODO: This is not adding one-hot
        self.one_hot = one_hot
        env_oss = env.observation_space.shape[0]
        self.num_act = env.action_space.n if self.one_hot else 1 
        self.observation_space = spaces.Box(-np.inf, np.inf,
                                            shape=(env_oss+self.num_act,),
                                            dtype=np.float32)
    def reset(self, step_fn=None, **kwargs):
        if step_fn is None:
            step_fn = self.step
        return self.env.reset(step_fn=step_fn, **kwargs)

    def step(self, action):
        actions = np.zeros(self.num_act) #this will be a vector of length 1 if not onehot encoded
        if self.one_hot:
            actions[action] = 1
        else:
            actions[0] = action
        obs, reward, done, trunc, info = self.env.step(action)
        obs = np.concatenate((obs, actions))
        return obs, reward, done, trunc, info
