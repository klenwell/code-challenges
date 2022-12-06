"""
Advent of Code 2022 - Day 6
https://adventofcode.com/2022/day/6

References:
2981
2980
2982
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-06.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.input_lines[0]
        print(len(input))

        for n in range(len(input)):
            if n < 3:
                continue

            c1 = input[n-3]
            c2 = input[n-2]
            c3 = input[n-1]
            c4 = input[n]
            word = '{}{}{}{}'.format(c1,c2,c3,c4)

            if len(set(word)) == len(word):
                print(word, n)
                return n+1

    @property
    def second(self):
        input = self.input_lines[0]
        print(len(input))
        #input = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'

        for n in range(len(input)):
            if n < 14:
                continue

            word = input[n-14:n]
            #print(word)
            #breakpoint()

            if len(set(word)) == len(word):
                print(word, len(word), n)
                return n

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


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
