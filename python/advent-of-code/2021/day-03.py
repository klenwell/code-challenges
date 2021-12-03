"""
Advent of Code 2021 - Day 03
https://adventofcode.com/2021/day/3

## PUZZLE
TBA
"""
from os.path import dirname, join as path_join

ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')


def extract_report():
    with open(INPUT_FILE) as file:
        entries = file.readlines()
        return [e.strip() for e in entries]


def rows_to_bit_columns(rows):
    bit_columns = []
    num_cols = len(rows[0])

    for n in range(num_cols):
        bit_column = []

        for row in rows:
            bit = int(row[n])
            bit_column.append(bit)

        bit_columns.append(bit_column)

    return bit_columns


def parse_bit_columns(bit_columns):
    gamma_bits = []
    epsilon_bits = []
    to_bit_str = lambda bits: ''.join([str(b) for b in bits])

    for bit_list in bit_columns:
        gamma_bit = bit_list_to_gamma_bit(bit_list)
        epsilon_bit = 1 if gamma_bit == 0 else 0
        gamma_bits.append(gamma_bit)
        epsilon_bits.append(epsilon_bit)

    gamma = int(to_bit_str(gamma_bits), 2)
    epsilon = int(to_bit_str(epsilon_bits), 2)

    return gamma, epsilon


def bit_list_to_gamma_bit(bit_list):
    zero_count = len([bit for bit in bit_list if bit == 0])
    one_count = len([bit for bit in bit_list if bit == 1])

    if zero_count > one_count:
        return 0
    else:
        return 1


def solve_pt1():
    rows = extract_report()
    bit_columns = rows_to_bit_columns(rows)
    gamma, epsilon = parse_bit_columns(bit_columns)
    return gamma * epsilon


def solve_pt2():
    """https://adventofcode.com/2021/day/3#part2"""
    pass


#
# Main
#
solution = solve_pt1()
print("pt 1 solution: {}".format(solution))

solution = solve_pt2()
print("pt 2 solution: {}".format(solution))
