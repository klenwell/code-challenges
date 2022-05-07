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

    def test_expects_to_repeat_endlessly(self):
        # Arrange
        in_repeat_loop = itertools.repeat('nom')
        sequence = []

        # Act
        while len(sequence) < 100:
            sequence.append(next(in_repeat_loop))

        # Assert
        self.assertEqual(len(sequence), 100)
        self.assertEqual(sequence[0], 'nom')

    def test_expects_to_repeat_three_times(self):
        # Arrange
        in_repeat_loop = itertools.repeat('nom', 3)
        sequence = []
        keep_repeating = True

        # Act
        while keep_repeating:
            try:
                sequence.append(next(in_repeat_loop))
            except StopIteration:
                keep_repeating = False

        # Assert
        self.assertEqual(len(sequence), 3)
        self.assertEqual(sequence, ['nom'] * 3)
        self.assertEqual(sequence, list(itertools.repeat('nom', 3)))

    def test_accumulate(self):
        accumulation = list(itertools.accumulate([1, 2, 3, 4]))
        self.assertEqual(accumulation, [1, 3, 6, 10])

    def test_chain(self):
        chained = list(itertools.chain('ABC', 'DEF', 'GHI'))
        self.assertEqual(chained, list('ABCDEFGHI'))

    def test_chain_from_iterable(self):
        iterable = ['ABC', 'DEF', 'GHI']
        chained = list(itertools.chain.from_iterable(iterable))
        self.assertEqual(chained, list('ABCDEFGHI'))

    def test_compress(self):
        data = ['vanilla', 'chocolate', 'strawberry', 'cookies and cream']
        selectors = [True, False, True, True]
        compressed = list(itertools.compress(data, selectors))
        self.assertEqual(compressed, ['vanilla', 'strawberry', 'cookies and cream'])

    def test_dropwhile(self):
        predicate = lambda v: v == None
        sequence = [None, None, False, True, None, False]
        undropped = list(itertools.dropwhile(predicate, sequence))
        self.assertEqual(undropped, [False, True, None, False])

    def test_filterfalse(self):
        exclude = lambda v: v == None
        sequence = [None, None, False, True, None, True, False]
        filtered = list(itertools.filterfalse(exclude, sequence))
        self.assertEqual(filtered, [False, True, True, False])

#
# Main
#
if __name__ == '__main__':
    unittest.main()
