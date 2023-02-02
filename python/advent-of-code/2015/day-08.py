"""
Advent of Code 2015 - Day 8
https://adventofcode.com/2015/day/8

Day 8: Matchsticks
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class DigitalSantaList:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def decoded_str_delta(self):
        return self.raw_str_len - self.decoded_str_len

    @cached_property
    def encoded_str_delta(self):
        return self.encoded_str_len - self.raw_str_len

    @cached_property
    def raw_str_len(self):
        return sum([len(line) for line in self.lines])

    @cached_property
    def decoded_str_len(self):
        # For part 1
        return sum([self.decoded_line_len(line) for line in self.lines])

    @cached_property
    def encoded_str_len(self):
        # For part 2
        return sum([self.encoded_line_len(line) for line in self.lines])

    @cached_property
    def lines(self):
        return self.input.split('\n')

    def decoded_line_len(self, line):
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

    def encoded_line_len(self, line):
        bs = '\\'
        dq = '"'
        chrs = [dq, bs, bs]

        for n, chr in enumerate(list(line[1:-1])):
            if chr in (bs, dq):
                chrs += [bs, chr]
            else:
                chrs.append(chr)

        chrs += [bs, dq, dq]
        return len(chrs)


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
        assert santa_list.decoded_str_delta < 1379, santa_list.decoded_str_delta
        return santa_list.decoded_str_delta

    @property
    def second(self):
        input = self.file_input.strip()
        santa_list = DigitalSantaList(input)
        return santa_list.encoded_str_delta

    #
    # Tests
    #
    @property
    def test1(self):
        expected_lens = [(2, 0), (5, 3), (10, 7), (6, 1)]
        input = self.TEST_INPUT
        santa_list = DigitalSantaList(input)

        for n, line in enumerate(santa_list.lines):
            exp_str_len, exp_dec_len = expected_lens[n]
            dec_len = santa_list.decoded_line_len(line)
            assert len(line) == exp_str_len, (line, len(line), exp_str_len)
            assert dec_len == exp_dec_len, (line, dec_len, exp_dec_len)

        assert len(santa_list.input)
        assert santa_list.decoded_str_len == 11, santa_list.decoded_str_len
        assert santa_list.decoded_str_delta == 12, santa_list.decoded_str_delta

        # Edge Cases
        edge_cases = [
            # str, str_len, mem_len
            (r'"bmcfkidxyilgoy\\xmu\"ig\\qg"', 29, 24),
            (r'"rq\\\"mohnjdf\\xv\\hrnosdtmvxot"', 33, 27),
            (r'"fdan\\\x9e"', 12, 6),
            (r'"\"pa\\x\x18od\\emgje\\"', 24, 15)
        ]

        for line, exp_str_len, exp_dec_len in edge_cases:
            str_len = len(line)
            dec_len = santa_list.decoded_line_len(line)
            assert str_len == exp_str_len, (line, str_len, exp_str_len)
            assert dec_len == exp_dec_len, (line, dec_len, exp_dec_len)

        return 'passed'

    @property
    def test2(self):
        expected_lens = [(2, 6), (5, 9), (10, 16), (6, 11)]
        input = self.TEST_INPUT
        santa_list = DigitalSantaList(input)

        for n, line in enumerate(santa_list.lines):
            exp_str_len, exp_enc_len = expected_lens[n]
            enc_len = santa_list.encoded_line_len(line)
            assert len(line) == exp_str_len, (line, len(line), exp_str_len)
            assert enc_len == exp_enc_len, (line, enc_len, exp_enc_len)

        assert len(santa_list.input)
        assert santa_list.encoded_str_len == 42, santa_list.encoded_str_len
        assert santa_list.encoded_str_delta == 19, santa_list.encoded_str_delta
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
