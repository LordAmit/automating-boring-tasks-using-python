from typing import List
from duplicate_image_finder import __version__
import duplicate_image_finder.duplicate_finder as dup


def diff_int(m: int, n: int):
    return abs(m-n)


class TestClass:

    def test_version(self):
        assert __version__ == '0.1.0'

    def test_find_groups1(self):
        threshold: int = 4
        input: List = [1, 2, 3, 7, 8, 19, 20, 21]
        #             [0, 1, 2, 3, 4,  5,  6,  7]

        expected_output = [(0, 2), (3, 4), (5, 7)]

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output

    def test_find_groups2(self):
        threshold: int = 4

        input: List = [1, 2, 3, 7, 8, 19, 20, 21, 70]
        #              [0, 1, 2, 3, 4,  5,  6,  7,  8]

        expected_output = [(0, 2), (3, 4), (5, 7)]

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output

    def test_find_groups3(self):
        threshold: int = 4

        input: List = []

        expected_output = []

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output

    def test_find_groups4(self):
        threshold: int = 4

        input: List = [1, 2, 3, 4]
        #              [0, 1, 2, 3]

        expected_output = [(0, 3)]

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output

    def test_find_groups5(self):
        threshold: int = 4

        input: List = [1, 1, 1, 1]
        #              [0, 1, 2, 3]

        expected_output = [(0, 3)]

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output

    def test_find_groups6(self):
        threshold: int = 4

        input: List = [1, 10, 20, 21, 30, 40]
        #              [0,  1,  2,  3,  4,  5]
        expected_output = [(2, 3)]

        output = dup.find_groups(input, diff_int, threshold)
        print(output)
        print(expected_output)
        assert output == expected_output
