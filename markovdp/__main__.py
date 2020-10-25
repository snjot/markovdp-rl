import argparse
from typing import List

from markovdp.drawer import CuiDrawer, GuiDrawer, NullDrawer
from markovdp.game import Game


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="seconds to delay each step",
    )
    parser.add_argument(
        "--games",
        type=int,
        default=10,
        help="number of games",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--gui", action="store_true")
    return parser.parse_args()


def create_grid() -> List[List[int]]:
    return [[0, 0, 0, 1], [0, 9, 0, -1], [0, 0, 0, 0]]


def select_drawer(is_verbose: bool, is_gui: bool):
    if is_gui:
        return GuiDrawer()
    if is_verbose:
        return CuiDrawer()
    return NullDrawer()


def main(delay: float, n_games: int, is_verbose: bool, is_gui: bool):
    grid = create_grid()

    drawer = select_drawer(is_verbose, is_gui)
    game = Game(drawer, grid, n_games, delay)

    game.play()


if __name__ == "__main__":
    args = parse_args()
    main(args.delay, args.games, args.verbose, args.gui)
