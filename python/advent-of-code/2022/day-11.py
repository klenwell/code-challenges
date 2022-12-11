"""
Advent of Code 2022 - Day 11
https://adventofcode.com/2022/day/11
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

from math import floor


INPUT_FILE = path_join(INPUT_DIR, 'day-11.txt')

TEST_INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


class Monkey:
    def __init__(self, notes):
        self.number = None
        self.op = []
        self.items = []
        self.test = None
        self.true = None
        self.false = None
        self.inspections = 0
        self.parse_notes(notes)

    def take_turn(self, monkeys):
        while self.items:
            item = self.items.pop(0)
            self.inspect(item)
            self.throw(item, monkeys)

    def inspect(self, item):
        # After each monkey inspects an item but before it tests your worry level,
        # your relief that the monkey's inspection didn't damage the item causes
        # your worry level to be divided by three and rounded down to the nearest integer.
        self.inspections += 1
        item = self.change_worry_level(item)
        #print(item)round
        item.worry = int(floor(item.worry / 3.0))

    def change_worry_level(self, item):
        if self.op[0] != 'old':
            raise ValueError('Unexpected op[0]: {}'.format(self.op[0]))

        op = self.op[1]
        val = item.worry if self.op[-1] == 'old' else int(self.op[-1])

        if op == '+':
            item.worry = item.worry + val
        elif op == '*':
            item.worry = item.worry * val
        else:
            raise ValueError('Unexpected op: {}'.format(op))

        return item

    def throw(self, item, monkeys):
        val = self.test[-1]
        if item.worry % val == 0:
            throws_to = self.true
        else:
            throws_to = self.false

        monkey = [m for m in monkeys if m.number == throws_to][0]

        #print('THROW', self.number, 'to', monkey.number, item.worry)
        monkey.items.append(item)

    def parse_notes(self, notes):
        notes = notes.strip()
        lines = [l.strip() for l in notes.split('\n')]
        self.number = int(lines[0].split(' ')[-1][:-1])
        self.items = self.parse_items(lines[1])
        #print(self.number, self.items)
        self.op = self.parse_op(lines[2])
        self.test = self.parse_test(lines[3])
        self.true = int(lines[4].split(' ')[-1])
        self.false = int(lines[5].split(' ')[-1])
        #print(lines)

    def parse_items(self, line):
        item_csv = line.split(':')[-1]
        items = [Item(v) for v in item_csv.split(',')]
        return items

    def parse_op(self, line):
        line = line.split('=')[-1].strip()
        return line.split(' ')

    def parse_test(self, line):
        words = line.split(' ')
        return [words[1], int(words[-1])]

    def __repr__(self):
        items = ', '.join([str(i.worry) for i in self.items])
        return "<Monkey #{} items={} op='{}' test={} t={} f={} inspections={}>".format(
            self.number, items, self.op, self.test, self.true, self.false, self.inspections)


class Item:
    def __init__(self, input):
        self.worry = int(input.strip())

    def __repr__(self):
        return "<Item worry={}>".format(self.worry)


class EfficientMonkey(Monkey):
    def parse_items(self, line):
        item_csv = line.split(':')[-1]
        items = [EfficientItem(v) for v in item_csv.split(',')]
        return items

    def inspect(self, item):
        # No more relief at end of each round
        self.inspections += 1
        item = self.change_worry_level(item)
        #print(item)roundop_val
        #item.worry = int(floor(item.worry / 3.0))

    def change_worry_level(self, item):
        if self.op[0] != 'old':
            raise ValueError('Unexpected op[0]: {}'.format(self.op[0]))

        op = self.op[1]
        val = self.op[-1]

        if op == '+':
            item.add(val)
        elif op == '*':
            item.mult(val)

        return item

    def throw(self, item, monkeys):
        div_val = self.test[-1]

        if item.lcd_counts[div_val] > 0:
            throws_to = self.true
        else:
            throws_to = self.false

        monkey = [m for m in monkeys if m.number == throws_to][0]

        #print('THROW', self.number, 'to', monkey.number, item.worry)
        monkey.items.append(item)


class EfficientItem:
    DIVISIBLES = [13, 19, 5, 2, 17, 11, 7, 3] + [23]

    def __init__(self, input):
        value = int(input.strip())
        self.lcd_counts = dict([(lcd, 0) for lcd in self.DIVISIBLES])
        self.decompose(value)

    @property
    def worry(self):
        value = 1

        for lcd, count in self.lcd_counts.items():
            if count == 0:
                continue
            value = value * lcd * count

        return value

    def mult(self, value):
        if value == 'old':
            for lcd in self.DIVISIBLES:
                self.lcd_counts[lcd] += 1
        else:
            value = int(value)
            self.lcd_counts[value] += 1

    def add(self, value):
        value = self.worry + int(value)
        self.decompose(value)

    def decompose(self, value):
        for lcd in self.DIVISIBLES:
            if value % lcd == 0:
                self.lcd_counts[lcd] = value / lcd
            else:
                self.lcd_counts[lcd] = 0

    def __repr__(self):
        return "<Item lcd_counts={}>".format(self.lcd_counts)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        rounds = 20
        notebook = TEST_INPUT

        monkeys_notes = notebook.split('\n\n')
        print(monkeys_notes)
        monkeys = [Monkey(monkey_notes) for monkey_notes in monkeys_notes]
        print(monkeys)
        print(monkeys[0].items[0])

        for n in range(rounds):
            print('Round', n)
            for monkey in monkeys:
                monkey.take_turn(monkeys)
            print(monkeys)
            #breakpoint()

        active_monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)
        print(active_monkeys)
        monkey_business = active_monkeys[0].inspections * active_monkeys[1].inspections
        return monkey_business

    @property
    def first(self):
        rounds = 20
        notebook = self.input

        monkeys_notes = notebook.split('\n\n')
        monkeys = [Monkey(monkey_notes) for monkey_notes in monkeys_notes]

        for n in range(rounds):
            print('Round', n)
            for monkey in monkeys:
                monkey.take_turn(monkeys)
            #breakpoint()

        active_monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)
        print(active_monkeys)
        monkey_business = active_monkeys[0].inspections * active_monkeys[1].inspections
        return monkey_business

    @property
    def test2(self):
        rounds = 10000
        notebook = TEST_INPUT

        monkeys_notes = notebook.split('\n\n')
        monkeys = [EfficientMonkey(monkey_notes) for monkey_notes in monkeys_notes]

        for n in range(rounds):
            print('Round', n)
            for monkey in monkeys:
                monkey.take_turn(monkeys)
            #breakpoint()

        active_monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)
        print(active_monkeys)
        monkey_business = active_monkeys[0].inspections * active_monkeys[1].inspections
        return monkey_business

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("test 2 solution: {}".format(solution.test2))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
