from typing import Dict, List

from markovdp.action import Action
from markovdp.environment import Environment
from markovdp.planner.base import Planner
from markovdp.state import State


class ValueIterationPlanner(Planner):
    def __init__(self, env: Environment):
        super().__init__(env)

    def plan(self, gamma: float = 0.9, threshold: float = 0.0001) -> List[List[float]]:
        self.initialize()
        actions: List[Action] = self._env.actions
        V: Dict[State, float] = {}
        for s in self._env.states:
            V[s] = 0.0

        while True:
            delta: float = 0.0
            self._log.append(self.dict_to_grid(V))
            for s in V:
                if not self._env.can_action_at(s):
                    continue
                expected_rewards: List[float] = []
                for a in actions:
                    r: float = 0.0
                    for prob, next_state, reward in self.transitions_at(s, a):
                        r += prob * (reward + gamma * V[next_state])
                    expected_rewards.append(r)
                max_reward: float = max(expected_rewards)
                delta = max(delta, abs(max_reward - V[s]))
                V[s] = max_reward

            if delta < threshold:
                break

        V_grid = self.dict_to_grid(V)
        return V_grid
