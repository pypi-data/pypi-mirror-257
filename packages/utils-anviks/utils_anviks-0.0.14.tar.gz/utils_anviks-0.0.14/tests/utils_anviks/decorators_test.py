import os
from functools import wraps

from utils_package.src.utils_anviks._decorators import read_data


def test_read_data():
    matrix = [
        [5, 8, 2, 3, 7, 9, 8, 6, 3, 8, 2],
        [2, 7, 6, 9, 4, 8, 7, 3, 9, 4, 8],
        [9, 7, 0, 8, 9, 8, 6, 0, 3, 4, 7],
        [2, 6, 7, 3, 9, 4, 8, 0, 9, 2, 3]
    ]

    matrix_string = "\n".join(
        "".join(
            str(element) for element in row
        )
        for row in matrix
    )

    if not os.path.exists("../files"):
        os.mkdir("../files")

    with open("../files/number_matrix.txt", "w") as f:
        f.write(matrix_string)

    @read_data(filename="../files/number_matrix.txt", sep2="", _class=int)
    def foo(data: list[list[int]]):
        return data

    assert foo() == matrix


def test_read_data_add_type_hint():
    def bar(data):
        def inn(func):
            def wrap(*args):
                pass

            return wrap

        return inn

    @read_data("../files/number_matrix.txt", sep2="", _class=int)
    # @bar("data: set[int]")
    def foo(  # data: set[int]
            data: set[int], boo: int):
        return data, boo

    print(foo(1))
