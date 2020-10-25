import time
from typing import List

from markovdp.agent import Agent
from markovdp.drawer import Drawer
from markovdp.environment import Environment


class Game:
    def __init__(self, drawer: Drawer, grid: List[List[int]], n_games: int, delay: float):
        self._drawer = drawer
        self._n_games = n_games
        self._delay = delay
        self._env = Environment(grid)
        self._agent = Agent(self._env)

    def play(self):
        for i in range(self._n_games):
            state = self._env.reset()
            total_reward = 0.0
            done = False

            state_history = [state]

            while not done:
                action = self._agent.policy(state)
                next_state, reward, done = self._env.step(action)

                time.sleep(self._delay)
                self._drawer.draw(self._env, next_state, action)

                total_reward += reward
                state = next_state

                state_history.append(state)

            # if is_verbose:
            #     print(f"History: {state_history}")
            print(f"Episode {i}: Agent gets {total_reward} reward.")
