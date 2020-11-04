from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from markovdp.action import Action
from markovdp.agent.base import Agent
from markovdp.environment import Environment
from markovdp.planner import ValueIterationPlanner
from markovdp.state import State


class ValueIter(Agent):
    def __init__(self, env: Environment):
        self._actions: List[Action] = env.actions
        self._env = env
        self._planner = ValueIterationPlanner(env)
        self._V_grid = self._planner.plan(gamma=0.99)
        self._visualize()

    def policy(self, state: State) -> Action:
        values: Dict[Action, float] = {}

        up = state.row - 1
        if up < 0:
            values[Action.UP] = -100.0
        else:
            values[Action.UP] = self._V_grid[up][state.column]
            # Goal
            if self._env.get_grid((state.column, up)) == 1:
                values[Action.UP] = 100.0

        down = state.row + 1
        if down >= self._env.row_length:
            values[Action.DOWN] = -100.0
        else:
            values[Action.DOWN] = self._V_grid[state.row + 1][state.column]
            # Goal
            if self._env.get_grid((state.column, down)) == 1:
                values[Action.DOWN] = 100.0

        left = state.column - 1
        if left < 0:
            values[Action.LEFT] = -100.0
        else:
            values[Action.LEFT] = self._V_grid[state.row][left]
            # Goal
            if self._env.get_grid((left, state.row)) == 1:
                values[Action.LEFT] = 100.0

        right = state.column + 1
        if right >= self._env.column_length:
            values[Action.RIGHT] = -100.0
        else:
            values[Action.RIGHT] = self._V_grid[state.row][state.column + 1]
            # Goal
            if self._env.get_grid((right, state.row)) == 1:
                values[Action.RIGHT] = 100.0

        action: Action = max(values, key=values.get)  # type: ignore
        print(action, values[action])
        return action

    def _visualize(self):
        fig, ax = plt.subplots(figsize=(4, 3))
        sb.heatmap(np.array(self._V_grid), annot=True, cmap="Blues")
        plt.show()
