"""
Advent of Code 2015 - Day 8
https://adventofcode.com/2015/day/8
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class DigitalSantaList:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def storage_space(self):
        return self.str_length - self.mem_length

    @cached_property
    def str_length(self):
        return sum([len(line) for line in self.lines])

    @cached_property
    def mem_length(self):
        return sum([self.line_mem_length(line) for line in self.lines])

    @cached_property
    def lines(self):
        return self.input.split('\n')

    def line_mem_length(self, line):
        mem_chrs = []
        chrs = list(line[1:-1])

        while chrs:
            chr = chrs.pop(0)

            if chr != '\\':
                mem_chrs.append(chr)
                continue

            # Figure out escape chrs
            next_chr = chrs.pop(0)
            if next_chr == 'x':
                chrs.pop(0)
                chrs.pop(0)
                mem_chrs.append('_')
            else:
                mem_chrs.append(next_chr)

        return len(mem_chrs)

    def line_mem_length_v1(self, line):
        if line.count(r'\\x') > 0:
            print(line)
            breakpoint()
        literal_len = len(line)
        quote_len = 2
        slash_len = line.count(r'\\')
        dbl_quote_len = line.count(r'\"')
        hex_len = line.count(r'\x') * 3
        add_back = line.count(r'\\x') * 3
        return literal_len - quote_len - slash_len - dbl_quote_len - hex_len + add_back


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')

    TEST_INPUT = r"""
""
"abc"
"aaa\"aaa"
"\x27"
"""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input.strip()
        santa_list = DigitalSantaList(input)
        for line in santa_list.lines[-16:]:
            raw_len = len(line)
            mem_len = santa_list.line_mem_length(line)
            print(line, raw_len, mem_len)
        assert santa_list.storage_space < 1379, santa_list.storage_space
        return santa_list.storage_space

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        expected_lens = [(2, 0), (5, 3), (10, 7), (6, 1)]
        input = self.TEST_INPUT
        santa_list = DigitalSantaList(input)

        for n, line in enumerate(santa_list.lines):
            print(n, line, len(line))
            exp_str_len, exp_mem_len = expected_lens[n]
            mem_len = santa_list.line_mem_length(line)
            assert len(line) == exp_str_len, (line, len(line), exp_str_len)
            assert mem_len == exp_mem_len, (line, mem_len, exp_mem_len)

        assert len(santa_list.input)
        assert santa_list.mem_length == sum([l for _, l in expected_lens]), santa_list.mem_length
        assert santa_list.storage_space == 12, santa_list.storage_space

        # Edge Cases
        edge_cases = [
            # str, str_len, mem_len
            (r'"bmcfkidxyilgoy\\xmu\"ig\\qg"', 29, 24),
            (r'"rq\\\"mohnjdf\\xv\\hrnosdtmvxot"', 33, 27),
            (r'"fdan\\\x9e"', 12, 6),
            (r'"\"pa\\x\x18od\\emgje\\"', 24, 15)
        ]

        for line, exp_str_len, exp_mem_len in edge_cases:
            str_len = len(line)
            mem_len = santa_list.line_mem_length(line)
            assert str_len == exp_str_len, (line, str_len, exp_str_len)
            assert mem_len == exp_mem_len, (line, mem_len, exp_mem_len)

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE, 'r') as file:
            return file.read().strip()


#
# Main
#
problem = DailyPuzzle()
problem.solve()
