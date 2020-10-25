from markovdp.action import Action
from markovdp.drawer.base import Drawer
from markovdp.environment import Environment
from markovdp.state import State


class CuiDrawer(Drawer):
    def draw(self, env: Environment, state: State, action: Action):
        print(f"Action: {action}")
        print(f"State: {state}")
