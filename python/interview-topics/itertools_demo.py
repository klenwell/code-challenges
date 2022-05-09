"""
A quick introduction to Python itertools.

https://docs.python.org/3/library/itertools.html
"""
import itertools
import unittest
import math
from dataclasses import dataclass


class IterToolsTest(unittest.TestCase):
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
        predicate = lambda v: v is None
        sequence = [None, None, False, True, None, False]
        undropped = list(itertools.dropwhile(predicate, sequence))
        self.assertEqual(undropped, [False, True, None, False])

    def test_filterfalse(self):
        exclude = lambda v: v is None
        sequence = [None, None, False, True, None, True, False]
        filtered = list(itertools.filterfalse(exclude, sequence))
        self.assertEqual(filtered, [False, True, True, False])

    def test_groupsby(self):
        results = 'HHTHTTTHHTHHHHH'
        uniquekeys = []
        streaks = []

        for k, g in itertools.groupby(results):
            uniquekeys.append(k)
            streaks.append(list(g))

        self.assertEqual(uniquekeys, list('HTHTHTH'))
        self.assertEqual(streaks[-1], list('HHHHH'))

    def test_expects_groupby_to_not_work_for_dataclasses(self):
        # See https://stackoverflow.com/a/68011508/1093087
        # Arrange
        @dataclass
        class Student:
            grade: str = ''

        iterable = [
            Student(grade='B'),
            Student(grade='C'),
            Student(grade='A'),
            Student(grade='F'),
            Student(grade='C')
        ]

        uniquekeys = []
        groups = []

        # Act
        keyfunc = lambda s: s.grade
        for k, g in itertools.groupby(iterable, keyfunc):
            uniquekeys.append(k)
            groups.append(list(g))

        # Assert
        self.assertEqual(sorted(uniquekeys), list('ABCCF'))
        self.assertNotEqual(len(groups), 4)

    def test_islice(self):
        sequence = ['bun', 'lettuce', 'tomato', 'meat', 'bun']
        start = 1
        stop = len(sequence) - 1    # Note: -1 is invalid

        slices = list(itertools.islice(sequence, start, stop))

        self.assertEqual(slices, ['lettuce', 'tomato', 'meat'])
        self.assertNotIn('bun', slices)

    def test_starmap(self):
        seq = [(2, 5), (3, 2), (10, 3)]
        func = pow
        results = list(itertools.starmap(func, seq))
        self.assertEqual([32, 9, 1000], results)

    def test_takewhile(self):
        predicate = lambda v: v is not None
        sequence = [False, True, None, False]
        undropped = list(itertools.takewhile(predicate, sequence))
        self.assertEqual(undropped, [False, True])

    def test_tee(self):
        iterable = ['Ready', 'Set', 'Go']
        steps = []

        iterables = itertools.tee(iterable, 2)
        for seq in iterables:
            for step in seq:
                steps.append(step)

        self.assertEqual(len(steps), 6)
        self.assertEqual(steps, ['Ready', 'Set', 'Go', 'Ready', 'Set', 'Go'])

    def test_zip_longest(self):
        seq1 = list('ABC')
        seq2 = list(range(1, 10))
        seq3 = ['Alice', 'Bob', 'Charles', 'Diana']

        zipped = list(itertools.zip_longest(seq1, seq2, seq3))

        self.assertEqual(zipped[0], ('A', 1, 'Alice'))
        self.assertEqual(zipped[-1], (None, 9, None))


class IterToolsInfiniteIteratorsTest(unittest.TestCase):
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


class IterToolsCombinatricTest(unittest.TestCase):
    def test_product(self):
        letters = list('ABC')
        nums = [1, 2, 3]

        cartesian_product = list(itertools.product(letters, nums))

        self.assertEqual(len(cartesian_product), 9)
        self.assertEqual(cartesian_product[0], ('A', 1))
        self.assertEqual(cartesian_product[-1], ('C', 3))

    def test_permutations(self):
        iterable = ['A', 'B', 'C', 1, 2, 3]

        permutations = list(itertools.permutations(iterable))

        self.assertEqual(len(permutations), math.factorial(len(iterable)))
        self.assertEqual(permutations[0], ('A', 'B', 'C', 1, 2, 3))
        self.assertEqual(permutations[-1], (3, 2, 1, 'C', 'B', 'A'))

    def test_combinations(self):
        iterable = ['A', 'B', 'C', 1, 2, 3]

        combinations = list(itertools.combinations(iterable, 3))

        self.assertEqual(len(combinations), 20)
        self.assertEqual(combinations[0], ('A', 'B', 'C'))
        self.assertEqual(combinations[-1], (1, 2, 3))

    def test_combinations_with_replacement(self):
        iterable = ['A', 'B', 'C', 1, 2, 3]

        combinations = list(itertools.combinations_with_replacement(iterable, 3))

        self.assertEqual(len(combinations), 56)
        self.assertEqual(combinations[0], ('A', 'A', 'A'))
        self.assertEqual(combinations[-1], (3, 3, 3))


#
# Main
#
if __name__ == '__main__':
    unittest.main()
