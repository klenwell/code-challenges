"""
Advent of Code 2022 - Day 8
https://adventofcode.com/2022/day/8

References:

"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')

TEST_INPUT = """\
30373
25512
65332
33549
35390"""


class TreeGrid:
    def __init__(self, input_rows):
        self.input_rows = input_rows

    @property
    def visible_trees(self):
        visible_trees = []

        for x, row in enumerate(self.rows):
            visible_trees += self.check_row(x, row)

        for y, col in enumerate(self.cols):
            visible_trees += self.check_col(y, col)

        return sorted(set(visible_trees))

    @property
    def all_trees(self):
        trees = []

        for x in range(len(self.rows)):
            for y in range(len(self.cols)):
                trees.append((x,y))

        return trees

    @property
    def highest_scenic_score(self):
        scores = []
        for tree in self.all_trees:
            score = self.compute_scenic_score(tree)
            scores.append(score)
        return max(scores)

    def compute_scenic_score(self, tree):
        left = self.look_left(tree)
        right = self.look_right(tree)
        up = self.look_up(tree)
        down = self.look_down(tree)
        return up * left * down * right

    def look_right(self, tree):
        score = 0
        x, y = tree
        row = self.rows[y]
        tree_ht = row[x]
        neighbors = row[x+1:]
        for ht in neighbors:
            score += 1
            if ht >= tree_ht:
                return score
        return score

    def look_left(self, tree):
        score = 0
        x, y = tree
        row = self.rows[y]
        tree_ht = row[x]
        neighbors = list(reversed(row[:x]))
        for ht in neighbors:
            score += 1
            if ht >= tree_ht:
                return score
        return score

    def look_down(self, tree):
        score = 0
        x, y = tree
        col = self.cols[x]
        tree_ht = col[y]
        neighbors = col[y+1:]
        for ht in neighbors:
            score += 1
            if ht >= tree_ht:
                return score
        return score

    def look_up(self, tree):
        score = 0
        x, y = tree
        col = self.cols[x]
        tree_ht = col[y]
        neighbors = list(reversed(col[:y]))
        for ht in neighbors:
            score += 1
            if ht >= tree_ht:
                return score
        return score


    @cached_property
    def rows(self):
        rows = []
        for input_row in self.input_rows:
            row = [int(n) for n in list(input_row)]
            rows.append(row)
        return rows

    @cached_property
    def cols(self):
        cols = []
        for n in range(len(self.rows)):
            col = []
            for row in self.rows:
                col.append(row[n])
            cols.append(col)
        return cols

    def check_row(self, x, row):
        visible_trees = []

        # Left Side
        high_tree = -1
        for y, tree_ht in enumerate(row):
            if tree_ht > high_tree:
                high_tree = tree_ht
                visible_trees.append((x, y))

        # Right Side
        high_tree = -1
        rev_row = reversed(row)
        for off_y, tree_ht in enumerate(rev_row):
            y = len(row) - off_y - 1
            if tree_ht > high_tree:
                high_tree = tree_ht
                visible_trees.append((x, y))

        #print(row, '->', list(set(visible_trees)))
        return list(set(visible_trees))

    def check_col(self, y, col):
        visible_trees = []

        # Left Side
        high_tree = -1
        for x, tree_ht in enumerate(col):
            if tree_ht > high_tree:
                high_tree = tree_ht
                visible_trees.append((x, y))

        # Right Side
        high_tree = -1
        rev_col = reversed(col)
        for off_x, tree_ht in enumerate(rev_col):
            x = len(col) - off_x - 1
            if tree_ht > high_tree:
                high_tree = tree_ht
                visible_trees.append((x, y))

        return list(set(visible_trees))


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file
        self.input_rows = []

    #
    # Solutions
    #
    @property
    def test(self):
        grid = TreeGrid(self.test_input_lines)
        #print(grid.rows)
        #print(grid.cols)
        return len(grid.visible_trees)

    @property
    def test2(self):
        grid = TreeGrid(self.test_input_lines)
        print(grid.all_trees)
        return grid.highest_scenic_score

    @property
    def first(self):
        grid = TreeGrid(self.input_lines)
        return len(grid.visible_trees)

    @property
    def second(self):
        grid = TreeGrid(self.input_lines)
        return grid.highest_scenic_score

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
print("test 1 solution: {}".format(solution.test))
print("test 2 solution: {}".format(solution.test2))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
