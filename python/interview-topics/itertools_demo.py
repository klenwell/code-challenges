"""
A quick introduction to Python itertools.

https://docs.python.org/3/library/itertools.html
"""
import itertools
import unittest


class IterToolsTest(unittest.TestCase):
    def test_expects_to_count_to_five(self):
        # Arrange
        in_count_loop = itertools.count(start=1, step=1)
        sequence = []

        # Act
        while len(sequence) < 5:
            sequence.append(next(in_count_loop))

        # Assert
        self.assertEqual(sequence, [1, 2, 3, 4, 5])

    def test_expects_to_count_by_twos(self):
        # Arrange
        in_count_loop = itertools.count(start=0, step=2)
        sequence = []

        # Act
        while len(sequence) < 5:
            sequence.append(next(in_count_loop))

        # Assert
        self.assertEqual(sequence, [0, 2, 4, 6, 8])

    def test_expects_to_cycle_three_times(self):
        # Arrange
        in_cycle_loop = itertools.cycle('ABCD')
        sequence = []

        # Act
        while sequence.count('D') < 3:
            sequence.append(next(in_cycle_loop))

        # Assert
        self.assertEqual(sequence.count('A'), 3)
        self.assertEqual(sequence.count('D'), 3)


#
# Main
#
if __name__ == '__main__':
    unittest.main()
