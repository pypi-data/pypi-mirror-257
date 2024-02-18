from collections.abc import Sequence
from typing import overload

# TODO: add support for adding ints as complex
class Coordinate2D:
    @overload
    def __init__(self, x: int, y: int):
        ...

    @overload
    def __init__(self, xy: Sequence[int, int]):
        ...

    @overload
    def __init__(self, xy: complex):
        ...

    def __init__(self, *args):
        error_message = f"given arguments {args} don't match any of the signatures."

        if len(args) == 1:
            if isinstance(args[0], complex):
                self.__x, self.__y = int(args[0].real), int(args[0].imag)
                return
            elif isinstance(args[0], Sequence):
                args = args[0]
            else:
                raise TypeError(error_message)

        if len(args) == 2 and all(isinstance(arg, int) for arg in args):
            self.__x, self.__y = args
        else:
            raise TypeError(error_message)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __add__(self, other):
        if isinstance(other, complex):
            return Coordinate2D(self.x + int(other.real), self.y + int(other.imag))
        elif isinstance(other, Sequence):
            return Coordinate2D(self.x + other[0], self.y + other[1])
        elif isinstance(other, Coordinate2D):
            return Coordinate2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, complex):
            return Coordinate2D(self.x - int(other.real), self.y - int(other.imag))
        elif isinstance(other, Sequence):
            return Coordinate2D(self.x - other[0], self.y - other[1])
        elif isinstance(other, Coordinate2D):
            return Coordinate2D(self.x - other.x, self.y - other.y)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def __truediv__(self, other):
        if not isinstance(other, Coordinate2D):
            raise TypeError("Division is only supported between Coordinate2D objects")

        denominator = other.x ** 2 + other.y ** 2
        if denominator == 0:
            raise ZeroDivisionError("Division by zero")

        numerator_x = self.x * other.x + self.y * other.y
        numerator_y = self.y * other.x - self.x * other.y

        return Coordinate2D(int(numerator_x / denominator), int(numerator_y / denominator))

    def __mod__(self, other):
        if isinstance(other, complex):
            return Coordinate2D(self.x % int(other.real), self.y % int(other.imag))
        elif isinstance(other, Sequence):
            return Coordinate2D(self.x % other[0], self.y % other[1])
        elif isinstance(other, Coordinate2D):
            return Coordinate2D(self.x % other.x, self.y % other.y)
        elif isinstance(other, int):
            return Coordinate2D(self.x % other, self.y % other)
        else:
            raise TypeError(f"unsupported operand type(s) for %: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def __complex__(self):
        return complex(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"


class Coordinate3D:
    @overload
    def __init__(self, x: int, y: int, z: int):
        ...

    @overload
    def __init__(self, xyz: Sequence[int, int, int]):
        ...

    def __init__(self, *args):
        error_message = f"given arguments {args} don't match any of the signatures."

        if len(args) == 1 and isinstance(args[0], Sequence):
            args = args[0]

        if len(args) != 3 or not all(isinstance(arg, int) for arg in args):
            raise TypeError(error_message)

        self.__x, self.__y, self.__z = args

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    def __add__(self, other):
        if isinstance(other, Sequence):
            return Coordinate3D(self.x + other[0], self.y + other[1], self.z + other[2])
        elif isinstance(other, Coordinate3D):
            return Coordinate3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, Sequence):
            return Coordinate3D(self.x - other[0], self.y - other[1], self.z - other[2])
        elif isinstance(other, Coordinate3D):
            return Coordinate3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def __mod__(self, other):
        if isinstance(other, Sequence):
            return Coordinate3D(self.x % other[0], self.y % other[1], self.z % other[2])
        elif isinstance(other, Coordinate3D):
            return Coordinate3D(self.x % other.x, self.y % other.y, self.z % other.z)
        elif isinstance(other, int):
            return Coordinate3D(self.x % other, self.y % other, self.z % other)
        else:
            raise TypeError(f"unsupported operand type(s) for %: '{self.__class__.__name__}' and '{type(other).__name__}'")

    def extract_height(self) -> tuple[Coordinate2D, int]:
        return Coordinate2D(self.x, self.y), self.z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})"


if __name__ == '__main__':
    print(Coordinate2D(0, -1) / Coordinate2D(1, 0))
    print(-1j / 1)

