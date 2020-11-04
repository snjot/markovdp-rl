import time
from typing import List, Type

from markovdp.agent import Agent, NoBrain, PolicyIter, ValueIter
from markovdp.drawer import Drawer
from markovdp.environment import Environment
from markovdp.state import State


def select_agent_class(method: str) -> Type[Agent]:
    if method == "PolicyIter":
        return PolicyIter
    elif method == "ValueIter":
        return ValueIter
    return NoBrain


class Game:
    def __init__(self, drawer: Drawer, grid: List[List[int]], n_games: int, delay: float, method: str):
        self._drawer = drawer
        self._n_games = n_games
        self._delay = delay
        self._env = Environment(grid)
        self._agent = select_agent_class(method)(self._env)

    def play(self):
        for i in range(self._n_games):
            state = self._env.reset()
            total_reward = 0.0
            done = False

            state_history = [state]

            while not done:
                state, done, total_reward = self.update(state, total_reward, state_history)
                time.sleep(self._delay)

            print(f"Episode {i}: Agent gets {total_reward} reward.")

    def update(self, state: State, total_reward: float, state_history: List[State]):
        action = self._agent.policy(state)
        next_state, reward, done = self._env.step(action)

        self._drawer.draw(self._env, next_state, action)

        total_reward += reward
        state = next_state

        state_history.append(state)

        return state, done, total_reward
