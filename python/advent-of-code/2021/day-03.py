"""
Advent of Code 2021 - Day 03
https://adventofcode.com/2021/day/3
"""
from os.path import dirname, join as path_join
from functools import cached_property


ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')


class DiagnosticReport:
    def __init__(self, input_file):
        self.input_file = input_file

    @property
    def power_consumption(self):
        return self.gamma_rate * self.epsilon_rate

    @property
    def life_support_rating(self):
        return self.oxygen_rating * self.co2_rating

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
    def gamma_rate(self):
        gamma_rate_bits = []

        for bits in self.columns:
            most_common_bit = self.most_common_bit(bits)
            gamma_rate_bits.append(most_common_bit)

        return self.bits_to_int(gamma_rate_bits)

    @property
    def epsilon_rate(self):
        epsilon_rate_bits = []

        for bits in self.columns:
            least_common_bit = self.least_common_bit(bits)
            epsilon_rate_bits.append(least_common_bit)

        return self.bits_to_int(epsilon_rate_bits)

    @property
    def oxygen_rating(self):
        filtered_rows = self.rows.copy()

        for n in self.col_nums:
            matching_rows = []
            match_bit = self.most_common_bit_by_column(filtered_rows, n)

            for row in filtered_rows:
                if self.row_to_bits(row)[n] == match_bit:
                    matching_rows.append(row)

            filtered_rows = matching_rows.copy()

            if len(filtered_rows) == 1:
                break

        return self.bits_to_int(filtered_rows[0])

    @property
    def co2_rating(self):
        filtered_rows = self.rows.copy()

        for n in self.col_nums:
            matching_rows = []
            match_bit = self.least_common_bit_by_column(filtered_rows, n)

            for row in filtered_rows:
                if self.row_to_bits(row)[n] == match_bit:
                    matching_rows.append(row)

            filtered_rows = matching_rows.copy()

            if len(filtered_rows) == 1:
                break

        return self.bits_to_int(filtered_rows[0])

    #
    # Methods
    #
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

    def most_common_bit_by_column(self, rows, col):
        col_bits = [int(row[col]) for row in rows]

        try:
            return self.most_common_bit(col_bits)
        except ValueError:
            return 1

    def least_common_bit_by_column(self, rows, col):
        col_bits = [int(row[col]) for row in rows]

        try:
            return self.least_common_bit(col_bits)
        except ValueError:
            return 0

    def row_to_bits(self, row):
        return [int(b) for b in list(row)]

    def bits_to_int(self, bits):
        bit_str = ''.join([str(b) for b in bits])
        return int(bit_str, 2)


#
# Main
#
report = DiagnosticReport(INPUT_FILE)
print("pt 1 solution: {}".format(report.power_consumption))
print("pt 2 solution: {}".format(report.life_support_rating))
