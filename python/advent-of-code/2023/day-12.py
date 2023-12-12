"""
Advent of Code 2023 - Day 12
https://adventofcode.com/2023/day/12
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class SpringDamageReport:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def arrangements_sum(self):
        sum = 0
        for record in self.records:
            sum += len(record.arrangement_count)
        return sum

    @cached_property
    def rows(self):
        rows = []
        for line in self.input.split('\n'):
            row = line.strip()
            rows.append(row)
        return rows

    @cached_property
    def records(self):
        records = []
        for row in self.rows:
            record = SpringRecord(row)
            records.append(record)
        return records


class SpringRecord:
    def __init__(self, row):
        self.row = row

    @cached_property
    def arrangement_count(self):
        return len(self.find_arrangements())

    @cached_property
    def conditions(self):
        conditions, _ = self.row.split(' ')
        return list(conditions.strip())

    @cached_property
    def groupings(self):
        counts = []
        _, groupings = self.row.split(' ')
        for count in groupings.strip().split(','):
            counts.append(int(count))
        return counts

    @cached_property
    def length(self):
        return len(self.conditions)

    @cached_property
    def unknowns(self):
        return [n for (n, condition) in enumerate(self.conditions) if condition == '?']

    @cached_property
    def damaged(self):
        return [n for (n, condition) in enumerate(self.conditions) if condition == '#']

    @cached_property
    def operational(self):
        return [n for (n, condition) in enumerate(self.conditions) if condition == '.']

    def find_arrangements(self):
        arrangements = []
        from itertools import permutations
        missing_damaged = sum(self.groupings) - len(self.damaged)
        for permutation in permutations(self.unknowns, missing_damaged):
            print(self.unknowns, missing_damaged, permutation)
            arrangement = RowArrangement(self, permutation)
            print(arrangement)
            if arrangement.is_possible():
                arrangements.append(arrangement)
        return arrangements


class RowArrangement:
    def __init__(self, record, damaged):
        self.record = record
        self.damaged = damaged

    @cached_property
    def conditions(self):
        row = []
        for n, condition in enumerate(self.record.conditions):
            if condition != '?':
                row.append(condition)

            if n in self.damaged:
                row.append('#')
            else:
                row.append('.')
        return row

    def is_possible(self):
        return False

    def __repr__(self):
        return f"<Arrangement {self.conditions}>"




class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-12.txt')

    TEST_INPUT = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        report = SpringDamageReport(input)
        assert report.arrangements_sum == 21, report.arrangements_sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
