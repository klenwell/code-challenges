"""
Advent of Code 2021 - Day 03
https://adventofcode.com/2021/day/3

## PUZZLE
TBA
"""
from os.path import dirname, join as path_join
from functools import cached_property

ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')


class DiagnosticReport:
    def __init__(self, input_file):
        self.input_file = input_file

    @cached_property
    def rows(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def col_nums(self):
        num_cols = len(self.rows[0])
        return list(range(num_cols))

    @cached_property
    def columns(self):
        columns = []

        for n in self.col_nums:
            bits = []

            for row in self.rows:
                bit = int(row[n])
                bits.append(bit)

            columns.append(bits)

        return columns

    @property
    def power_consumption(self):
        return self.gamma_rate * self.epsilon_rate

    @property
    def binary_gamma_rate(self):
        gamma_rate_bits = []

        for bits in self.columns:
            most_common_bit = self.most_common_bit(bits)
            gamma_rate_bits.append(most_common_bit)

        return ''.join([str(bit) for bit in gamma_rate_bits])

    @property
    def gamma_rate(self):
        return int(self.binary_gamma_rate, 2)

    @property
    def binary_epsilon_rate(self):
        epsilon_rate_bits = []

        for bits in self.columns:
            least_common_bit = self.least_common_bit(bits)
            epsilon_rate_bits.append(least_common_bit)

        return ''.join([str(bit) for bit in epsilon_rate_bits])

    @property
    def epsilon_rate(self):
        return int(self.binary_epsilon_rate, 2)

    def most_common_bit(self, bits):
        zero_count = len([bit for bit in bits if bit == 0])
        one_count = len([bit for bit in bits if bit == 1])

        if zero_count > one_count:
            return 0
        elif one_count > zero_count:
            return 1
        else:
            raise ValueError("0 and 1 bits equal")

    def least_common_bit(self, bits):
        return self.most_common_bit(bits) ^ 1



def extract_report():
    with open(INPUT_FILE) as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def rate_rows(rows, match_by, default_bit):
    num_cols = len(rows[0])
    reduced_rows = rows.copy()

    if match_by == 'most':
        match_bit_fx = most_common_bit_by_index
    else:
        match_bit_fx = least_common_bit_by_index

    for col in range(num_cols):
        matching_rows = []
        match_bit = match_bit_fx(reduced_rows, col)
        match_bit = match_bit if match_bit != 2 else default_bit

        for row in reduced_rows:
            bits = [int(b) for b in list(row)]
            if bits[col] == match_bit:
                matching_rows.append(row)

        reduced_rows = matching_rows.copy()

        if len(reduced_rows) == 1:
            break

    return bits_to_int(reduced_rows[0])


def most_common_bit_by_index(rows, index):
    index_bits = [int(row[index]) for row in rows]
    zero_count = len([bit for bit in index_bits if bit == 0])
    one_count = len([bit for bit in index_bits if bit == 1])

    if zero_count > one_count:
        return 0
    elif one_count > zero_count:
        return 1
    else:
        return 2


def least_common_bit_by_index(rows, index):
    bit = most_common_bit_by_index(rows, index)
    if bit == 2:
        return bit
    else:
        return bit ^ 1


def bits_to_int(bits):
    bit_str = ''.join([str(b) for b in bits])
    return int(bit_str, 2)


#
# Solutions
#
def solve_pt1():
    report = DiagnosticReport(INPUT_FILE)
    return report.power_consumption


def solve_pt2():
    """https://adventofcode.com/2021/day/3#part2"""
    rows = extract_report()
    oxy_rating = rate_rows(rows, 'most', 1)
    co2_rating = rate_rows(rows, 'least', 0)
    return oxy_rating * co2_rating


#
# Main
#
solution = solve_pt1()
print("pt 1 solution: {}".format(solution))

solution = solve_pt2()
print("pt 2 solution: {}".format(solution))
