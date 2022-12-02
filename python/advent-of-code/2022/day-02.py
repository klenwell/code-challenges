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

    def outcome(self, opp, you):
        # A, X = Rock
        # B, Y = Paper
        # C, Z = Scissors
        rock = 0
        paper = 1
        scissors = 2
        opp_map = {'A': rock, 'B': paper, 'C': scissors}
        you_map = {'X': rock, 'Y': paper, 'Z': scissors}

        opp_played = opp_map[opp]
        you_played = you_map[you]

        if opp_played == you_played:
            return 3

        if (you_played == rock and opp_played == scissors) or \
            (you_played == paper and opp_played == rock) or \
            (you_played == scissors and opp_played == paper):
            return 6

        return 0



#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
