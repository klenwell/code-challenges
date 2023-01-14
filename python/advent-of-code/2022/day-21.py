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


DEBUG = False


def verbose(*args):
    if not DEBUG:
        return


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

        verbose('translate', monkey, yelled, translation)
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


class PatchedMonkeyTranslator(MonkeyTranslator):
    def __init__(self, lines):
        self.lines = lines
        self.patched_monkeys = self.patch_monkeys(lines)

    def patch_monkeys(self, lines):
        monkeys = {}

        for line in lines:
            monkey, output = line.split(':')
            output = output.strip()

            # The modified operation for monkey root should be =
            if monkey == 'root':
                m1, op, m2 = output.split(' ')
                output = (m1, '=', m2)
                output = ' '.join(output)

            try:
                value = int(output)
            except ValueError:
                m1, op, m2 = output.split(' ')
                value = (m1, m2, op)

            # The number that appears after humn: in your input is now irrelevant.
            if monkey == 'humn':
                value = None

            monkeys[monkey] = value
        return monkeys

    def translate(self, monkey):
        yelled = self.patched_monkeys[monkey]
        verbose('translate', monkey, yelled)

        if type(yelled) is tuple:
            m1, m2, op = yelled
            if op == '=':
                translation = self.equate(m1, m2)
            else:
                translation = eval(f"{self.translate(m1)} {op} {self.translate(m2)}")
        else:
            translation = yelled

        verbose('translated', monkey, yelled, int(translation))
        return int(translation)

    def equate(self, m1, m2):
        verbose('equate', m1, m2)
        for monkey in (m1, m2):
            try:
                translation = self.translate(monkey)
                self.patched_monkeys[monkey] = translation
            except TypeError:
                unknown = monkey

        self.patched_monkeys[unknown] = self.solve_for(unknown, translation)
        verbose('equated', unknown, self.patched_monkeys[unknown])
        return self.patched_monkeys[unknown]

    def solve_for(self, unknown, value):
        verbose('solve_for', unknown, self.patched_monkeys[unknown], value)

        if self.patched_monkeys[unknown] is None:
            self.patched_monkeys[unknown] = value
            return value

        m1, m2, op = self.patched_monkeys[unknown]
        eq = {
            m1: None,
            m2: None
        }

        for monkey in (m1, m2):
            try:
                translation = self.translate(monkey)
                eq[monkey] = translation
                self.patched_monkeys[monkey] = translation
            except TypeError:
                eq[monkey] = monkey

        # This takes two operands (monkeys) from an equation and solves for the unknown
        # one (variable). That value then gets passed to solve_for so variable monkey's
        # formula equals value.
        var, var_value = self.isolate_variable(eq[m1], eq[m2], op, value)
        return self.solve_for(var, var_value)

    def isolate_variable(self, m1, m2, op, value):
        print('isolate_variable', (m1, op, m2), value)
        var = [v for v in (m1, m2) if not str(v).isdigit()][0]

        if m1 == var:
            if op == '+':
                var_value = value - m2
            elif op == '-':
                var_value = value + m2
            elif op == '/':
                var_value = value * m2
            elif op == '*':
                var_value = value // m2
        elif m2 == var:
            if op == '+':
                var_value = value - m1
            elif op == '-':
                var_value = m1 - value
            elif op == '/':
                var_value = m1 // value
            elif op == '*':
                var_value = value // m1

        print('isolated_variable', var, var_value)
        return var, var_value


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
        number = translator.translate('root')
        assert number == 63119856257960, number
        return number

    @property
    def test2(self):
        lines = self.test_input_lines
        t = PatchedMonkeyTranslator(lines)

        assert t.patched_monkeys['root'] == ('pppw', 'sjmn', '='), t.patched_monkeys['root']
        assert t.patched_monkeys['humn'] is None, t.patched_monkeys['humn']

        number = t.translate('root')

        assert t.patched_monkeys['humn'] == number, (t.patched_monkeys['humn'], number)
        assert number == 301, number
        return number

    @property
    def second(self):
        lines = self.input_lines
        translator = PatchedMonkeyTranslator(lines)
        number = translator.translate('root')
        assert translator.patched_monkeys['humn'] == number
        assert number != 7650891667780, "First wrong answer"
        assert number == 3006709232464, number
        return number

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
