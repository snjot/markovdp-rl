import abc
from typing import List

from markovdp.action import Action
from markovdp.environment import Environment
from markovdp.state import State


class Agent(abc.ABC):
    def __init__(self, env: Environment):
        self._actions: List[Action] = env.actions

    @abc.abstractmethod
    def policy(self, state: State) -> Action:
        pass
