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
        epsilon_bit = 1 if gamma_bit == 0 else 0    # or gamma_bit ^ 1
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


def rate_rows(rows, match_by, default_bit):
    num_cols = len(rows[0])
    reduced_rows = rows.copy()

    if match_by == 'most':
        match_bit_fx = most_common_bit_by_index
    else:
        match_bit_fx = least_common_bit_by_index


    for col in range(num_cols):
        match_bit = match_bit_fx(reduced_rows, col)
        matching_rows = []
        print(col, len(reduced_rows), reduced_rows[0], match_bit)

        match_bit = match_bit if match_bit != 2 else default_bit

        for row in reduced_rows:
            bits = [int(b) for b in list(row)]
            if bits[col] == match_bit:
                matching_rows.append(row)

        reduced_rows = matching_rows.copy()
        print(len(reduced_rows))

        if len(reduced_rows) == 1:
            break

    to_bit_str = lambda bits: ''.join([str(b) for b in bits])
    return int(to_bit_str(reduced_rows[0]), 2)


def extract_co2_rating(rows):
    pass


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


def solve_pt1():
    rows = extract_report()
    bit_columns = rows_to_bit_columns(rows)
    gamma, epsilon = parse_bit_columns(bit_columns)
    return gamma * epsilon


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
