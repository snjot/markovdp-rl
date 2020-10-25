from markovdp.action import Action
from markovdp.drawer.base import Drawer
from markovdp.environment import Environment
from markovdp.state import State


class NullDrawer(Drawer):
    def draw(self, env: Environment, state: State, action: Action):
        pass
