from typing import overload, TypeVar, Sequence

from utils_anviks import Coordinate2D

_T = TypeVar('_T')

class Grid:
    def __init__(self, grid: list[list[_T]]):
        self.grid = grid

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def rows(self):
        return self.grid

    @property
    def columns(self):
        return [list(col) for col in zip(*self.grid)]

    def find(self, value: _T) -> Coordinate2D | None:
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == value:
                    return Coordinate2D(i, j)
        return None

    @overload
    def __getitem__(self, coordinate: Coordinate2D) -> int:
        ...

    @overload
    def __getitem__(self, coordinate: Sequence[int]) -> int:
        ...

    @overload
    def __getitem__(self, coordinate: complex) -> int:
        ...

    def __getitem__(self, coordinate):
        if isinstance(coordinate, complex):
            return self.grid[int(coordinate.real)][int(coordinate.imag)]
        elif isinstance(coordinate, tuple):
            return self.grid[coordinate[0]][coordinate[1]]
        elif isinstance(coordinate, Coordinate2D):
            return self.grid[coordinate.x][coordinate.y]
        else:
            raise TypeError(f"unsupported operand type(s) for indexing: 'Grid' and '{type(coordinate).__name__}'")

    @overload
    def __setitem__(self, coordinate: Coordinate2D, value: _T):
        ...

    @overload
    def __setitem__(self, coordinate: Sequence[int], value: _T):
        ...

    @overload
    def __setitem__(self, coordinate: complex, value: _T):
        ...

    def __setitem__(self, coordinate, value):
        if isinstance(coordinate, complex):
            self.grid[int(coordinate.real)][int(coordinate.imag)] = value
        elif isinstance(coordinate, tuple):
            self.grid[coordinate[0]][coordinate[1]] = value
        elif isinstance(coordinate, Coordinate2D):
            self.grid[coordinate.x][coordinate.y] = value
        else:
            raise TypeError(f"unsupported operand type(s) for indexing: 'Grid' and '{type(coordinate).__name__}'")

    def __contains__(self, item):
        if isinstance(item, Coordinate2D):
            return 0 <= item.x < self.height and 0 <= item.y < self.width

    def __iter__(self):
        for row in self.grid:
            yield row

    def __repr__(self):
        return f"Grid(rows={len(self.grid)}, columns={len(self.grid[0])})"

    def __eq__(self, other):
        return self.grid == other.grid

