import abc


from markovdp.action import Action
from markovdp.environment import Environment
from markovdp.state import State


class Drawer(abc.ABC):
    @abc.abstractmethod
    def draw(self, env: Environment, state: State, action: Action):
        pass
