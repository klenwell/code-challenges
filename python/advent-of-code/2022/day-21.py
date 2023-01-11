"""
Advent of Code 2022 - Day 21
https://adventofcode.com/2022/day/21
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-21.txt')

TEST_INPUT = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


class MonkeyTranslator:
    def __init__(self, lines):
        self.lines = lines

    def translate(self, monkey):
        yelled = self.monkeys[monkey]

        if type(yelled) is tuple:
            m1, m2, op = yelled
            translation = eval(f"{self.translate(m1)} {op} {self.translate(m2)}")
        else:
            translation = yelled

        print('translate', monkey, yelled, translation)
        return int(translation)

    @property
    def monkeys(self):
        monkeys = {}

        for line in self.lines:
            monkey, output = line.split(':')
            output = output.strip()

            try:
                value = int(output)
            except ValueError:
                a, op, b = output.split(' ')
                value = (a, b, op)

            monkeys[monkey] = value

        return monkeys


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        lines = self.test_input_lines

        translator = MonkeyTranslator(lines)
        number = translator.translate('root')

        assert number == 152, number
        return number

    @property
    def first(self):
        lines = self.input_lines
        translator = MonkeyTranslator(lines)
        return translator.translate('root')

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
