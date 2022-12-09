"""
Advent of Code 2022 - Day 9
https://adventofcode.com/2022/day/9

References:
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-09.txt')

TEST_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


class Rope:
    def __init__(self):
        self.head = [0,0]
        self.tail = [0,0]
        self.tail_pts = [tuple(self.tail)]

    def simulate(self, motions):
        for motion in motions:
            dir, steps = motion.split(' ')
            print(dir, steps)
            for n in range(int(steps)):
                self.move_head(dir)
                print(motion, self.head, self.tail)

    def move_head(self, dir):
        if dir == 'R':
            self.head[0] += 1
        elif dir == 'L':
            self.head[0] -= 1
        elif dir == 'U':
            self.head[1] += 1
        elif dir == 'D':
            self.head[1] -= 1

        if not self.head_is_touching_tail():
            self.pull_tail()

        self.tail_pts.append(tuple(self.tail))

    def move_tail(self, dir):
        if dir == 'R':
            self.tail[0] += 1
        elif dir == 'L':
            self.tail[0] -= 1
        elif dir == 'U':
            self.tail[1] += 1
        elif dir == 'D':
            self.tail[1] -= 1

    def diff_head_tail(self):
        dx = self.head[0] - self.tail[0]
        dy = self.head[1] - self.tail[1]
        return (dx, dy)

    def head_is_touching_tail(self):
        dx, dy = self.diff_head_tail()
        return abs(dx) < 2 and abs(dy) < 2

    def pull_tail(self):
        dx, dy = self.diff_head_tail()

        if dx == 0 or dy == 0:
            self.move_tail_directionally(dx, dy)
        else:
            self.move_tail_diagnolly(dx, dy)

    def move_tail_directionally(self, dx, dy):
        if dx > 1:
            self.move_tail('R')
        elif dx < -1:
            self.move_tail('L')

        if dy > 1:
            self.move_tail('U')
        elif dy < -1:
            self.move_tail('D')

    def move_tail_diagnolly(self, dx, dy):
        if dx > 1:
            self.move_tail('R')
            self.move_tail('U') if dy > 0 else self.move_tail('D')
        elif dx < -1:
            self.move_tail('L')
            self.move_tail('U') if dy > 0 else self.move_tail('D')

        if dy > 1:
            self.move_tail('U')
            self.move_tail('R') if dx > 0 else self.move_tail('L')
        elif dy < -1:
            self.move_tail('D')
            self.move_tail('R') if dx > 0 else self.move_tail('L')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        motions = self.test_input_lines
        rope = Rope()
        rope.simulate(motions)
        print(rope.tail_pts)
        return len(set(rope.tail_pts))

    @property
    def test2(self):
        pass

    @property
    def first(self):
        motions = self.input_lines
        rope = Rope()
        rope.simulate(motions)
        print(rope.tail_pts)
        return len(set(rope.tail_pts))

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

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
