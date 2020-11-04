from __future__ import annotations


class State:
    def __init__(self, row: int = -1, column: int = -1):
        self._row: int = row
        self._column: int = column

    def __repr__(self) -> str:
        return f"<State: [{self._row}, {self._column}]>"

    def __hash__(self) -> int:
        return hash((self._row, self._column))

    def __eq__(self, other: State) -> bool:  # type: ignore
        return self._row == other._row and self._column == other._column

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    def clone(self) -> State:
        return State(self._row, self._column)

    def up(self) -> State:
        return State(self._row - 1, self._column)

    def down(self) -> State:
        return State(self._row + 1, self._column)

    def left(self) -> State:
        return State(self._row, self._column - 1)

    def right(self) -> State:
        return State(self._row, self._column + 1)
