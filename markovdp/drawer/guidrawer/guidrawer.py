import pyglet

from markovdp.action import Action
from markovdp.drawer.base import Drawer
from markovdp.drawer.guidrawer.window import GameWindow
from markovdp.environment import Environment
from markovdp.state import State


GRID_SIZE = 100


class GuiDrawer(Drawer):
    MAP_COLORS = {
        0: (255, 255, 255),
        1: (100, 100, 255),
        -1: (255, 100, 100),
        9: (0, 0, 0),
    }

    def __init__(self):
        self._window = GameWindow(GRID_SIZE * 4, GRID_SIZE * 3)
        self._window.set_caption("MARKOVDP-RL PLAYGROUND")
        pyglet.resource.path = ["../resources"]
        pyglet.resource.reindex()
        self._agent_image = pyglet.resource.image("agent.png")
        self._agent = pyglet.sprite.Sprite(img=self._agent_image, x=0, y=0)
        self._agent.scale = 0.5

    def draw(self, env: Environment, state: State, action: Action):
        print(f"Action: {action}")
        print(f"State: {state}")
        self._window.clear()

        for pos_y in range(env.row_length):
            for pos_x in range(env.column_length):
                grid = env.get_grid((pos_x, pos_y))
                grid_shape = pyglet.shapes.Rectangle(
                    x=pos_x * GRID_SIZE,
                    y=pos_y * GRID_SIZE,
                    width=GRID_SIZE,
                    height=GRID_SIZE,
                    color=GuiDrawer.MAP_COLORS[grid],
                )
                grid_shape.draw()
        self._agent.position = (state.column * GRID_SIZE, state.row * GRID_SIZE)
        self._agent.draw()
        self._tick()

    def _tick(self):
        pyglet.clock.tick()

        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event("on_draw")
            window.flip()
