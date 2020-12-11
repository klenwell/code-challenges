"""
Sudoku solver. (I've never done sudoku before.)

Interface dictated by sudoku.py.
"""
from math import floor


# Constants
SUDOKU_BOARD_CELLS = 81
EMPTY_CELL = 0


#
# GameBoard
#
class GameBoard:
    def __init__(self, *cell_values):
        # cell_values will be 80 item tuple representing board.
        self.cell_values = cell_values

    #
    # Public Methods
    #
    def next_moves(self):
        boards = []

        # Find first open cell
        cell_pos = self.first_open_cell_position()

        # Find valid values for open cell
        for value in range(1, 10):
            if self.is_valid_value_for_cell_position(cell_pos, value):
                board = self.update_cell(cell_pos, value)
                boards.append(board)

        # Return new board instances with valid values
        return boards

    def is_solved(self):
        return not any(cv == EMPTY_CELL for cv in self.cell_values)

    #
    # Private Methods
    #
    def first_open_cell_position(self):
        for n in range(SUDOKU_BOARD_CELLS):
            if self.cell_values[n] == EMPTY_CELL:
                return n
        return None

    def is_valid_value_for_cell_position(self, cell_pos, value):
        """A value is valid for a cell if it is valid for the given row, column,
        and mini-grid.
        """
        row_num = self.row_num_for_cell(cell_pos)
        col_num = self.col_num_for_cell(cell_pos)

        row_values = self.values_by_row_num(row_num)
        col_values = self.values_by_col_num(col_num)
        grid_values = self.grid_values_by_row_col_num(row_num, col_num)

        if value in row_values:
            return False

        if value in col_values:
            return False

        if value in grid_values:
            return False

        return True

    def row_num_for_cell(self, cell_pos):
        for row in range(9):
            min = row * 9
            max = min + 9
            if cell_pos in range(min, max):
                return row
        raise ValueError("Invalid cell position: {}".format(cell_pos))

    def col_num_for_cell(self, cell_pos):
        return cell_pos % 9

    def values_by_row_num(self, row_num):
        start = row_num * 9
        end = start + 9
        return self.cell_values[start:end]

    def values_by_col_num(self, col_num):
        values = []
        for row in range(9):
            row_offset = row * 9
            cell_idx = row_offset + col_num
            value = self.cell_values[cell_idx]
            values.append(value)
        return values

    def grid_values_by_row_col_num(self, row_num, col_num):
        values = []

        # Board is a 3x3 grid of 3x3 grids.
        grid_row_num = floor(row_num / 3) * 3
        grid_col_num = floor(col_num / 3) * 3

        for n in range(3):
            next_row_num = grid_row_num + n
            row_values = self.values_by_row_num(next_row_num)
            grid_values = row_values[grid_col_num:grid_col_num + 3]
            values += grid_values

        return values

    def update_cell(self, pos, value):
        cell_values = list(self.cell_values[:])
        cell_values[pos] = value
        return GameBoard(*cell_values)

    #
    # Magic Methods
    #
    def __eq__(self, other):
        return self.cell_values == other.cell_values

    def __repr__(self):
        return '<GameBoard cells={}>'.format(self.cell_values)


#
# Game
#
class Game:
    @staticmethod
    def solve(board):
        active_boards = [board]

        while active_boards:
            next_boards = []

            for board in active_boards:
                boards = board.next_moves()
                next_boards += boards

            for board in next_boards:
                if board.is_solved():
                    return board

            active_boards = next_boards[:]

        return None


#
# Main
#
if __name__ == '__main__':
    board = GameBoard(0, 0, 4, 0, 0, 0, 5, 0, 0,
                      0, 7, 0, 2, 0, 0, 3, 6, 0,
                      8, 0, 0, 0, 0, 1, 0, 0, 0,
                      6, 2, 9, 0, 0, 0, 0, 3, 0,
                      0, 0, 0, 0, 6, 0, 0, 0, 0,
                      0, 4, 0, 0, 0, 0, 6, 1, 8,
                      0, 0, 0, 7, 0, 0, 0, 0, 6,
                      0, 1, 3, 0, 0, 4, 0, 2, 0,
                      0, 0, 2, 0, 0, 0, 4, 0, 0)
    board = Game.solve(board)
    print(board)
