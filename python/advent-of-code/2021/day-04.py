"""
Advent of Code 2021 - Day 04
https://adventofcode.com/2021/day/4
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')


class BingoSubsystem:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def draws(self):
        line = self.input_lines[0]
        return [int(n) for n in line.split(',')]

    @cached_property
    def boards(self):
        boards = []
        rows = []

        for line in self.input_lines[1:]:
            if line == '':
                if rows:
                    board = BingoBoard(rows)
                    boards.append(board)
                    rows = []
            else:
                row = [int(n) for n in line.split()]
                rows.append(row)

        return boards

    @cached_property
    def winning_board(self):
        numbers = []

        for number in self.draws:
            numbers.append(number)

            for board in self.boards:
                if board.is_winner(numbers):
                    return board

        raise ValueError('winning board not found!')

    @cached_property
    def last_winning_board(self):
        numbers = []
        boards = [BingoBoard(board.rows) for board in self.boards]
        winning_boards = []

        for number in self.draws:
            numbers.append(number)
            losing_boards = []

            for board in boards:
                if board.is_winner(numbers):
                    winning_boards.append(board)
                else:
                    losing_boards.append(board)

            if not losing_boards:
                break

            boards = losing_boards

        if len(winning_boards) != len(self.boards):
            raise ValueError('Only {} of {} boards won!?', len(winning_boards), len(self.boards))

        return winning_boards[-1]


class BingoBoard:
    def __init__(self, rows):
        self.rows = rows
        self.called_numbers = []

    #
    # Properties
    #
    @cached_property
    def columns(self):
        columns = []

        for n in range(5):
            column = [row[n] for row in self.rows]
            columns.append(column)

        return columns

    @cached_property
    def all_squares(self):
        numbers = []

        for row in self.rows:
            for n in row:
                numbers.append(n)

        return numbers

    @property
    def score(self):
        if not self.is_winner(self.called_numbers):
            raise ValueError("This board is not a winner!")

        unmarked_numbers = set(self.all_squares) - set(self.called_numbers)
        return sum(unmarked_numbers) * self.called_numbers[-1]

    #
    # Methods
    #
    def is_winner(self, called_numbers):
        self.called_numbers = called_numbers

        for row in self.rows:
            if not (set(row) - set(called_numbers)):
                return True

        for column in self.columns:
            if not (set(column) - set(called_numbers)):
                return True

        return False


#
# Main
#
bingo = BingoSubsystem(INPUT_FILE)
print("pt 1 solution: {}".format(bingo.winning_board.score))
print("pt 2 solution: {}".format(bingo.last_winning_board.score))
