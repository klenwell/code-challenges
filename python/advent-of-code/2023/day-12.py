"""
Advent of Code 2023 - Day 12
https://adventofcode.com/2023/day/12
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class SpringDamageReport:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def arrangements_sum(self):
        sum = 0
        for record in self.records:
            print(f"{record.row} {record.arrangement_count} {sum}")
            sum += record.arrangement_count
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
    def damaged_group_sizes(self):
        sizes = []
        _, groups = self.row.split(' ')
        for size in groups.strip().split(','):
            sizes.append(int(size))
        return sizes

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

    @cached_property
    def damaged_spring_count(self):
        return sum(self.damaged_group_sizes)

    @cached_property
    def damaged_springs_missing(self):
        return self.damaged_spring_count - len(self.damaged)

    @cached_property
    def damaged_segments(self):
        segments = []
        for n, _ in enumerate(self.damaged_group_sizes):
            segment = RowSegment(n, self)
            segments.append(segment)
        return segments

    @cached_property
    def damaged_index_combos(self):
        import itertools as it
        combos = []
        indexes = [seg.indexes for seg in self.damaged_segments]
        print('combo', len(self.damaged_segments))

        for combo in it.product(*indexes):
            info(f"{indexes}, {combo}", 1000)
            combos.append(tuple(sorted(combo)))

        return list(set(combos))

        #return list(set([tuple(sorted(combo)) for combo in it.product(*indexes)]))

    def find_arrangements(self):
        arrangements = []

        # Groups -> Segments -> Indexes -> Combos
        # Permutate fill spot arrangements from blocks
        for damaged_index_combo in self.damaged_index_combos:

            arrangement = RowArrangement(self, damaged_index_combo)
            if arrangement.is_valid():
                #print('->', damaged_index_combo, arrangement, arrangement.is_valid())
                arrangements.append(arrangement)
        return arrangements

    def find_arrangements_naively(self):
        arrangements = []
        missing_damaged = sum(self.groupings) - len(self.damaged)

        # TODO: reduce the search space
        # Consider ???????##?????##???? 1,1,11,3
        for permutation in self.unique_permutations(self.unknowns, missing_damaged):

            #print(self.unknowns, missing_damaged, permutation)
            arrangement = RowArrangement(self, permutation)
            if arrangement.is_valid():
                #print(arrangement)
                #breakpoint()
                arrangements.append(arrangement)
        return arrangements

    def unique_permutations(self, iterable, r):
        # https://stackoverflow.com/q/6284396
        from itertools import permutations
        max = 10000000
        n = 0
        perms = set()
        for p in permutations(iterable, r):
            info(f"{n} {self.row} {iterable} {p}", 10000)
            t = tuple(sorted(p))
            perms.add(t)
            n += 1
            if n > max:
                raise Exception("Think harder, Homer")
        return list(perms)

    def __repr__(self):
        return f"<SpringRecord length={self.length} {self.row} count={self.arrangement_count}>"


class RowSegment:
    def __init__(self, group_index, record):
        self.number = group_index
        self.group_size = record.damaged_group_sizes[group_index]
        self.record = record

    @cached_property
    def start_index(self):
        return self.previous_segment_length

    @cached_property
    def end_index(self):
        next_group_sizes = self.record.damaged_group_sizes[self.number+1:]
        next_segment_len = sum(next_group_sizes) + len(next_group_sizes)
        return self.record.length - next_segment_len - 1

    @cached_property
    def range(self):
        return range(self.start_index, self.end_index+1)

    @cached_property
    def indexes(self):
        end = self.end_index + 1
        end = end - self.group_size + 1
        #print(self.end_index, end, end + 1)
        return range(self.start_index, end)

    @cached_property
    def length(self):
        return self.end_index + 1 - self.start_index

    @cached_property
    def previous_segment_length(self):
        prev_group_sizes = self.record.damaged_group_sizes[:self.number]
        return sum(prev_group_sizes) + len(prev_group_sizes)

    def __repr__(self):
        start = self.start_index
        end = self.end_index
        indexes = list(self.indexes)
        return f"<RowSegment [{start}, {end}] indexes={indexes}>"


class RowArrangement:
    def __init__(self, record, damaged_index_combo):
        self.record = record
        self.damaged_index_combo = damaged_index_combo

    @cached_property
    def damaged_index_size_pairs(self):
        return list(zip(self.damaged_index_combo, self.record.damaged_group_sizes))

    @cached_property
    def damaged_indexes(self):
        indexes = []
        for damaged_index, group_size in self.damaged_index_size_pairs:
            end_index = damaged_index + group_size
            group_indexes = list(range(damaged_index, end_index))
            indexes += group_indexes
        return sorted(indexes)

    def is_valid(self):
        #print(self.damaged_index_combo_conflicts_with_record(), self.segments_touch())
        if self.damaged_index_combo_conflicts_with_record():
            return False
        if self.segments_touch():
            return False
        return self.damaged_group_sizes == self.record.damaged_group_sizes

    def segments_touch(self):
        prev_segment_end = -2
        for damaged_index, group_size in self.damaged_index_size_pairs:
            #print(prev_segment_end, damaged_index - 2)
            if damaged_index <= prev_segment_end:
                return True
            prev_segment_end = damaged_index + group_size
        return False

    def damaged_index_combo_conflicts_with_record(self):
        for damaged_index, group_size in self.damaged_index_size_pairs:
            if self.damaged_group_conflicts_with_record(damaged_index, group_size):
                return True
        return False

    def damaged_group_conflicts_with_record(self, damaged_index, group_size):
        segment_end = damaged_index + group_size
        row_segment = self.record.conditions[damaged_index:segment_end]

        for condition in row_segment:
            #print(row_segment, condition, condition not in ['?', '#'])
            if condition not in ['?', '#']:
                return True

        return False

    @cached_property
    def conditions(self):
        row = []
        for index, condition in enumerate(self.record.conditions):
            #print(index, self.damaged_indexes)
            if condition in ('.', '#'):
                row.append(condition)
            elif condition == '?' and index in self.damaged_indexes:
                row.append('#')
            else:
                row.append('.')
        return row

    @cached_property
    def row(self):
        return ''.join(self.conditions)

    @cached_property
    def damaged_group_sizes(self):
        counts = []
        groupings = self.row.split('.')
        for group in groupings:
            if '#' in group:
                counts.append(len(group))
        return counts

    def __repr__(self):
        return f"<Arrangement {self.row} {self.damaged_group_sizes}>"


class FoldedRecord(SpringRecord):
    def __init__(self, row):
        self.folded_record = SpringRecord(row)
        conditions = self.unfold_conditions(self.folded_record.conditions)
        groups = self.unfold_groups(self.folded_record.damaged_group_sizes)
        row = f"{conditions} {groups}"
        super().__init__(row)

    @cached_property
    def arrangement_count(self):
        folded_count = len(self.folded_record.find_arrangements())
        return folded_count**5

    def unfold_conditions(self, conditions):
        condition_list = []
        condition_str = ''.join(conditions)
        for n in range(5):
            condition_list.append(condition_str)
        return '?'.join(condition_list)

    def unfold_groups(self, group_sizes):
        group_list = []
        group_str = ','.join([str(n) for n in group_sizes])
        for n in range(5):
            group_list.append(group_str)
        return ','.join(group_list)

    def __repr__(self):
        return f"<SpringRecord length={self.length} {self.row} count={self.arrangement_count}>"



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
        report = SpringDamageReport(input)
        return report.arrangements_sum

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        row = '?#?#?#?#?#?#?#? 1,3,1,6'
        expected = 1
        record = SpringRecord(row)
        print(record)
        assert record.arrangement_count == expected, record.arrangement_count

        expected_arrangements = (
            ('???.### 1,1,3', 1),
            ('.??..??...?##. 1,1,3', 4),
            ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
            ('????.#...#... 4,1,1', 1),
            ('????.######..#####. 1,6,5', 4),
            ('?###???????? 3,2,1', 10)
        )
        for input, expected in expected_arrangements:
            record = SpringRecord(input)
            assert record.arrangement_count == expected, record

        row = '?###???????? 3,2,1'
        #row = '???????##?????##???? 1,1,11,3'
        record = SpringRecord(row)
        print(record)
        print(record.damaged_segments)
        print(len(list(record.damaged_index_combos)))
        segment = record.damaged_segments[1]
        assert segment.start_index == 4, segment
        assert segment.end_index == 9, segment
        assert segment.length == 6, segment
        assert segment.indexes == range(4,9), segment

        arrangement = RowArrangement(record, [1, 5, 11])
        assert arrangement.is_valid(), arrangement

        print(record.conditions, record.damaged_group_sizes)
        assert record.arrangement_count == 10, record.arrangement_count



        input = self.TEST_INPUT
        report = SpringDamageReport(input)
        assert report.arrangements_sum == 21, report.arrangements_sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT

        input = '???.### 1,1,3'
        record = FoldedRecord(input)
        assert record.arrangement_count == 1, record

        input = '.??..??...?##. 1,1,3'
        record = FoldedRecord(input)
        assert record.arrangement_count == 506250, record

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
