"""
Advent of Code 2022 - Day 2
https://adventofcode.com/2022/day/2
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-02.txt')


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
            opp, you = line.split(' ')
            total_score += self.score_game(opp, you)
        return total_score

    @property
    def second(self):
        total_score = 0
        for line in self.input_lines:
            opp, outcome = line.split(' ')
            you = self.pick_move(opp, outcome)
            total_score += self.score_game(opp, you)
        return total_score

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
    def score_game(self, opp, you):
        score = 0
        shape_score = {'X': 1, 'Y': 2, 'Z': 3}

        score += self.outcome(opp, you)
        score += shape_score[you]
        return score

    def outcome(self, opp, you):
        if you == self.draw(opp):
            return 3
        elif you == self.win(opp):
            return 6
        else:
            return 0

    def pick_move(self, opp, outcome):
        outcome_map = {'X': 'lose', 'Y': 'draw', 'Z': 'win'}
        end = outcome_map[outcome]

        if end == 'draw':
            return self.draw(opp)
        elif end == 'lose':
            return self.lose(opp)
        else:
            return self.win(opp)

    def draw(self, opp):
        map = {
            'A': 'X',
            'B': 'Y',
            'C': 'Z'
        }
        return map[opp]

    def lose(self, opp):
        map = {
            'A': 'Z',
            'B': 'X',
            'C': 'Y'
        }
        return map[opp]

    def win(self, opp):
        map = {
            'A': 'Y',
            'B': 'Z',
            'C': 'X'
        }
        return map[opp]


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
