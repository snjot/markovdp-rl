import argparse
import time
from typing import List

from markovdp.agent import Agent
from markovdp.environment import Environment


N_GAMES = 10


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="seconds to delay each step",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def create_grid() -> List[List[int]]:
    return [[0, 0, 0, 1], [0, 9, 0, -1], [0, 0, 0, 0]]


def main(delay: float, is_verbose: bool):
    grid = create_grid()
    env = Environment(grid)
    agent = Agent(env)

    for i in range(N_GAMES):
        if is_verbose:
            print(f"-- GAME {i} START --")
        state = env.reset()
        total_reward = 0.0
        done = False

        state_history = [state]

        while not done:
            action = agent.policy(state)
            next_state, reward, done = env.step(action)
            time.sleep(delay)
            if is_verbose:
                print(f"Action: {action}")
                print(f"State: {next_state}")

            total_reward += reward
            state = next_state

            state_history.append(state)

        if is_verbose:
            print(f"History: {state_history}")
        print(f"Episode {i}: Agent gets {total_reward} reward.")


if __name__ == "__main__":
    args = parse_args()
    main(args.delay, args.verbose)
