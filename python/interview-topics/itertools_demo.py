"""
A quick introduction to Python itertools.

https://docs.python.org/3/library/itertools.html
"""
from itertools import count
import unittest


class IterToolsTest(unittest.TestCase):
    def test_expects_to_count_to_five(self):
        # Arrange
        in_count_loop = count(start=1, step=1)
        sequence = []

        # Act
        while len(sequence) < 5:
            sequence.append(next(in_count_loop))

        # Assert
        self.assertEqual(sequence, [1, 2, 3, 4, 5])

    def test_expects_to_count_by_twos(self):
        # Arrange
        in_count_loop = count(start=0, step=2)
        sequence = []

        # Act
        while len(sequence) < 5:
            sequence.append(next(in_count_loop))

        # Assert
        self.assertEqual(sequence, [0, 2, 4, 6, 8])


if __name__ == '__main__':
    unittest.main()
