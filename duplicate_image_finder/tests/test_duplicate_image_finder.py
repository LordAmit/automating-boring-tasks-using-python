from typing import List
from duplicate_image_finder import __version__
import duplicate_image_finder.duplicate_finder as dup


class TestClass:
    def test_version(self):
        assert __version__ == '0.1.0'

    def test_find_groups1(self):
        threshold: int = 4
        input1: List = [1, 2, 3, 7, 8, 19, 20, 21]
        #              [0, 1, 2, 3, 4,  5,  6,  7]

        expected_output1 = [(0, 2), (3, 4), (5, 7)]

        output = dup.find_groups(input1, threshold)
        print(output)
        print(expected_output1)
        assert output == expected_output1

    def test_find_groups2(self):
        threshold: int = 4

        input2: List = [1, 2, 3, 7, 8, 19, 20, 21, 70]
        #              [0, 1, 2, 3, 4,  5,  6,  7,  8]

        expected_output2 = [(0, 2), (3, 4), (5, 7)]

        output = dup.find_groups(input2, threshold)
        print(output)
        print(expected_output2)
        assert output == expected_output2

    def test_find_groups3(self):
        threshold: int = 4

        input3: List = []

        expected_output3 = []

        output = dup.find_groups(input3, threshold)
        print(output)
        print(expected_output3)
        assert output == expected_output3

    def test_find_groups4(self):
        threshold: int = 4

        input4: List = [1, 2, 3, 4]
        #              [0, 1, 2, 3]

        expected_output4 = [(0, 3)]

        output = dup.find_groups(input4, threshold)
        print(output)
        print(expected_output4)
        assert output == expected_output4

    def test_find_groups5(self):
        threshold: int = 4

        input5: List = [1, 1, 1, 1]
        #              [0, 1, 2, 3]

        expected_output5 = [(0, 3)]

        output = dup.find_groups(input5, threshold)
        print(output)
        print(expected_output5)
        assert output == expected_output5
