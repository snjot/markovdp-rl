from typing import List

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from markovdp.action import Action
from markovdp.agent.base import Agent
from markovdp.environment import Environment
from markovdp.planner import PolicyIterationPlanner
from markovdp.state import State


class PolicyIter(Agent):
    def __init__(self, env: Environment):
        self._actions: List[Action] = env.actions
        self._env = env
        self._planner = PolicyIterationPlanner(env)
        self._V_grid = self._planner.plan(gamma=0.99)
        self._visualize()

    def policy(self, state: State) -> Action:
        return self._planner.choose_action(state)

    def _visualize(self):
        fig, ax = plt.subplots(figsize=(4, 3))
        sb.heatmap(np.array(self._V_grid), annot=True, cmap="Blues")
        plt.show()
