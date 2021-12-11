"""
Advent of Code 2021 - Day 10
https://adventofcode.com/2021/day/10
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-10.txt')
CHUNK_CLOSE_CHARS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
SYNTAX_ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
# Invert mapping: https://stackoverflow.com/a/483833/1093087
CHUNK_OPEN_CHARS = {v: k for k, v in CHUNK_CLOSE_CHARS.items()}


class IncompleteChunkError(Exception): pass


class CorruptChunkError(Exception):
    @property
    def score(self):
        return SYNTAX_ERROR_SCORE[str(self)]


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        total_score = 0

        for line in self.input_lines:
            try:
                self.parse_chunks(line)
            except CorruptChunkError as e:
                total_score += e.score
            except IncompleteChunkError:
                pass

        return total_score

    @property
    def second(self):
        # Collect incomplete lines
        incomplete_lines = []
        for line in self.input_lines:
            try:
                self.parse_chunks(line)
            except CorruptChunkError:
                pass
            except IncompleteChunkError:
                incomplete_lines.append(line)

        # Score incomplete lines
        scores = []
        for incomplete_line in incomplete_lines:
            score = self.score_incomplete_line(incomplete_line)
            scores.append(score)

        # Find middle score
        middle_idx = len(scores) // 2
        middle_score = sorted(scores)[middle_idx]
        return middle_score

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #
    def score_incomplete_line(self, line):
        score = 0

        # Build incomplete stack
        stack = []
        for char in list(line):
            if char in CHUNK_CLOSE_CHARS.keys():
                open_char = stack.pop()
            else:
                stack.append(char)

        # Complete stack
        end_stack = []
        while len(stack) > 0:
            open_char = stack.pop()
            close_char = CHUNK_OPEN_CHARS[open_char]
            end_stack.append(close_char)

        # Score completion stack
        char_scores = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }
        for char in end_stack:
            score *= 5
            score += char_scores[char]

        return score

    def parse_chunks(self, line):
        chunks = 0
        stack = []

        for char in list(line):
            if char in CHUNK_CLOSE_CHARS.keys():
                open_char = stack.pop()
                if open_char != CHUNK_CLOSE_CHARS[char]:
                    raise CorruptChunkError(char)
                chunks += 1
            else:
                stack.append(char)

        if len(stack) != 0:
            raise IncompleteChunkError(stack)
        else:
            return chunks


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
