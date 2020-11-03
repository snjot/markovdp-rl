import abc
from typing import Dict, Iterator, List, Tuple

from markovdp.action import Action
from markovdp.environment import Environment
from markovdp.state import State


class Planner(abc.ABC):
    def __init__(self, env: Environment):
        self._env = env
        self._log: List[List[List[float]]] = []

    def initialize(self):
        self._env.reset()
        self._log = []

    @abc.abstractmethod
    def plan(self, gamma: float = 0.9, threshold: float = 0.0001) -> List[List[float]]:
        pass

    def transitions_at(self, state: State, action: Action) -> Iterator[Tuple[float, State, float]]:
        transition_probs: Dict[State, float] = self._env.transit_func(state, action)
        for next_state, prob in transition_probs.items():
            reward, _ = self._env.reward_func(next_state)
            yield prob, next_state, reward

    def dict_to_grid(self, state_reward_dict: Dict[State, float]) -> List[List[float]]:
        grid: List[List[float]] = []
        for i in range(self._env.row_length):
            row: List[float] = [0.0] * self._env.column_length
            grid.append(row)
        for s, reward in state_reward_dict.items():
            grid[s.row][s.column] = reward

        return grid
