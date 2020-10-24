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
        default=0.5,
        help="seconds to delay each step",
    )
    return parser.parse_args()


def create_grid() -> List[List[int]]:
    return [[0, 0, 0, 1], [0, 9, 0, -1], [0, 0, 0, 0]]


def main(delay: float):
    grid = create_grid()
    env = Environment(grid)
    agent = Agent(env)

    for i in range(N_GAMES):
        print(f"-- GAME {i} START --")
        state = env.reset()
        total_reward = 0.0
        done = False

        state_history = [state]

        while not done:
            action = agent.policy(state)
            print(f"Action: {action}")

            next_state, reward, done = env.step(action)
            time.sleep(delay)
            print(f"State: {next_state}")

            total_reward += reward
            state = next_state

            state_history.append(state)

        print(f"History: {state_history}")
        print(f"Episode {i}: Agent gets {total_reward} reward.")


if __name__ == "__main__":
    args = parse_args()
    main(args.delay)
