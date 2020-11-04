from typing import Dict, List

import numpy as np

from markovdp.action import Action
from markovdp.environment import Environment
from markovdp.planner.base import Planner
from markovdp.state import State


class PolicyIterationPlanner(Planner):
    def __init__(self, env: Environment):
        super().__init__(env)
        self._policy: Dict[State, Dict[Action, float]] = {}

    def initialize(self):
        super().initialize()
        self._policy: Dict[State, float] = {}
        actions: List[Action] = self._env.actions
        states: List[State] = self._env.states
        for s in states:
            self._policy[s] = {}
            for a in actions:
                self._policy[s][a] = 1 / len(actions)

    def choose_action(self, state: State) -> Action:
        policy_in_state = self._policy[state]
        return np.random.choice(list(policy_in_state.keys()), p=list(policy_in_state.values()))

    def plan(self, gamma: float = 0.9, threshold: float = 0.0001) -> List[List[float]]:
        self.initialize()
        states: List[State] = self._env.states
        actions: List[Action] = self._env.actions

        while True:
            update_stable = True
            V: Dict[State, float] = self._estimate_by_policy(gamma, threshold)
            self._log.append(self.dict_to_grid(V))

            for s in states:
                policy_action: Action = self._take_max_action(self._policy[s])

                action_rewards: Dict[Action, float] = {}
                for a in actions:
                    r: float = 0.0
                    for prob, next_state, reward in self.transitions_at(s, a):
                        r += prob * (reward + gamma * V[next_state])
                    action_rewards[a] = r
                best_action: Action = self._take_max_action(action_rewards)
                if policy_action != best_action:
                    update_stable = False

                for a in self._policy[s]:
                    prob = 1 if a == best_action else 0
                    self._policy[s][a] = prob

            if update_stable:
                break

        V_grid: List[List[float]] = self.dict_to_grid(V)
        return V_grid

    def _take_max_action(self, action_value_dict: Dict[Action, float]) -> Action:
        return max(action_value_dict, key=action_value_dict.get)  # type: ignore

    def _estimate_by_policy(self, gamma: float, threshold: float) -> Dict[State, float]:
        V: Dict[State, float] = {}
        for s in self._env.states:
            V[s] = 0.0

        while True:
            delta: float = 0.0
            for s in V:
                expected_rewards: List[float] = []
                for a, action_prob in self._policy[s].items():
                    r = 0.0
                    for prob, next_state, reward in self.transitions_at(s, a):
                        r += action_prob * prob * (reward + gamma * V[next_state])
                    expected_rewards.append(r)
                value: float = sum(expected_rewards)
                delta = max(delta, abs(value - V[s]))
                V[s] = value
            if delta < threshold:
                break

        return V
