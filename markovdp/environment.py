from typing import Dict, List, Tuple

import numpy as np

from markovdp.action import Action
from markovdp.state import State


class Environment:
    def __init__(self, grid: List[List[int]], move_prob: float = 0.8):
        self._grid: List[List[int]] = grid  # 0: ordinary / -1: damage / 1: reward / 9: block
        self._agent_state: State = State()
        self._default_reward: float = -0.04
        self._move_prob: float = move_prob
        self.reset()

    @property
    def row_length(self) -> int:
        return len(self._grid)

    @property
    def column_length(self) -> int:
        return len(self._grid[0])

    @property
    def actions(self) -> List[Action]:
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

    @property
    def states(self) -> List[State]:
        states = []
        for row in range(self.row_length):
            for column in range(self.column_length):
                if self._grid[row][column] != 9:
                    states.append(State(row, column))
        return states

    def get_grid(self, position: Tuple[int, int]):
        return self._grid[position[1]][position[0]]

    def can_action_at(self, state: State) -> bool:
        if self._grid[state._row][state._column] == 0:
            return True
        else:
            return False

    def transit_func(self, state: State, action: Action) -> Dict[State, float]:
        transition_probs: Dict[State, float] = {}
        if not self.can_action_at(state):
            return transition_probs

        opposite_direction = Action(action.value * -1)

        for a in self.actions:
            prob: float = 0.0
            if a == action:
                prob = self._move_prob
            elif a != opposite_direction:
                prob = (1 - self._move_prob) / 2

            next_state = self._move(state, a)
            if next_state not in transition_probs:
                transition_probs[next_state] = prob
            else:
                transition_probs[next_state] += prob

        return transition_probs

    def reward_func(self, state: State) -> Tuple[float, bool]:
        reward = self._default_reward
        done = False

        attribute = self._grid[state.row][state.column]
        if attribute == 1:
            reward = 1.0
            done = True
        elif attribute == -1:
            reward = -1.0
            done = True

        return reward, done

    def reset(self) -> State:
        self._agent_state = State(self.row_length - 1, 0)
        return self._agent_state

    def step(self, action: Action) -> Tuple[State, float, bool]:
        next_state, reward, done = self.transit(self._agent_state, action)
        if not done:
            self._agent_state = next_state

        return next_state, reward, done

    def transit(self, state: State, action: Action) -> Tuple[State, float, bool]:
        transition_probs = self.transit_func(state, action)
        if len(transition_probs) == 0:
            return state, 0.0, True

        next_states = []
        probs = []
        for state, prob in transition_probs.items():
            next_states.append(state)
            probs.append(prob)

        next_state = np.random.choice(next_states, p=probs)
        reward, done = self.reward_func(next_state)
        return next_state, reward, done

    def _move(self, state: State, action: Action) -> State:
        if not self.can_action_at(state):
            raise Exception("cannot move from here")

        if action == Action.UP:
            next_state = state.up()
        elif action == Action.DOWN:
            next_state = state.down()
        elif action == Action.LEFT:
            next_state = state.left()
        elif action == Action.RIGHT:
            next_state = state.right()

        if not (0 <= next_state.row < self.row_length):
            next_state = state
        if not (0 <= next_state.column < self.column_length):
            next_state = state

        if self._grid[next_state.row][next_state.column] == 9:
            next_state = state

        return next_state
