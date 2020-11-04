import random
from typing import List

from markovdp.action import Action
from markovdp.agent.base import Agent
from markovdp.environment import Environment
from markovdp.state import State


class NoBrain(Agent):
    def __init__(self, env: Environment):
        self._actions: List[Action] = env.actions

    def policy(self, state: State) -> Action:
        return random.choice(self._actions)
