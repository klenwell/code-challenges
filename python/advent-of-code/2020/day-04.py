"""
Advent of Code 2020 - Day 04
https://adventofcode.com/2020/day/4

Compare to https://github.com/tckmn/polyaoc-2020/blob/master/04/rb/04.rb (lol)
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')


class InvalidPassport(Exception): pass


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        valid_passports = 0
        for passport in self.passports:
            if self.is_valid(passport):
                valid_passports += 1
        return valid_passports

    @property
    def second(self):
        valid_passports = 0
        for passport in self.passports:
            if self.is_valid_v2(passport):
                valid_passports += 1
        return valid_passports

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def batches(self):
        with open(self.input_file, 'r') as file:
            data = file.read()
            return data.split("\n\n")

    @cached_property
    def passports(self):
        passports = []
        for batch in self.batches:
            passport = self.parse_passport(batch)
            passports.append(passport)
        return passports

    #
    # Methods
    #
    def parse_passport(self, batch):
        passport = {}
        fields = batch.split()
        for field in fields:
            k, v = field.split(':')
            passport[k] = v
        return passport

    def is_valid(self, passport):
        try:
            self.validate_presence(passport)
            return True
        except InvalidPassport:
            return False

    def is_valid_v2(self, passport):
        try:
            self.validate_presence(passport)
            self.validate_between(passport['byr'], 1920, 2002)
            self.validate_between(passport['iyr'], 2010, 2020)
            self.validate_between(passport['eyr'], 2020, 2030)
            self.validate_height(passport['hgt'])
            self.validate_hair(passport['hcl'])
            self.validate_eye(passport['ecl'])
            self.validate_pid(passport['pid'])
            return True
        except InvalidPassport:
            return False

    def validate_presence(self, passport):
        required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        fields = passport.keys()
        if len(set(required_fields) - set(fields)) > 0:
            raise InvalidPassport()

    def validate_between(self, value, min, max):
        num = int(value)
        if num < min or num > max:
            raise InvalidPassport('{} not between {} and {}'.format(value, min, max))

    def validate_height(self, value):
        valid_units = ['cm', 'in']
        unit = value[-2:]

        if unit not in valid_units:
            raise InvalidPassport('Invalid height: {}'.format(value))

        ht = int(value[:-2])
        if unit == 'cm':
            self.validate_between(ht, 150, 193)
        else:
            self.validate_between(ht, 59, 76)

    def validate_hair(self, value):
        if value[0] != '#':
            raise InvalidPassport('Invalid hair format: {}'.format(value))

        if len(value[1:]) != 6:
            raise InvalidPassport('Invalid hair color code: {}'.format(value))

        valid_chars = list('0123456789abcdef')
        for char in value[1:]:
            if char not in valid_chars:
                raise InvalidPassport('Invalid hair color char: {}'.format(value))

    def validate_eye(self, value):
        valid_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if value not in valid_colors:
            raise InvalidPassport('Invalid eye: {}'.format(value))

    def validate_pid(self, value):
        if not (value.isdigit() and len(value) == 9):
            raise InvalidPassport('Invalid pid: {}'.format(value))


class TestSuite:
    @staticmethod
    def run():
        suite = TestSuite()
        suite.test_validators()
        suite.expect_passports_to_be_valid()
        suite.expect_passports_to_be_invalid()
        print('All tests passed!')

    def __init__(self):
        self.solver = Solution(INPUT_FILE)

    def expect_passports_to_be_valid(self):
        batch_file = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
        batches = batch_file.split("\n\n")

        for batch in batches:
            passport = self.solver.parse_passport(batch)
            self.test_passport_validators(passport)

        return True

    def expect_passports_to_be_invalid(self):
        batch_file = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
        batches = batch_file.split("\n\n")

        for batch in batches:
            passport = self.solver.parse_passport(batch)

            try:
                self.test_passport_validators(passport)
                raise ValueError('Passport expect to be invalid: {}', passport)
            except InvalidPassport:
                pass

        return True

    def test_validators(self):
        """Need this to finally track down my bug. I had:
            if not value.isdigit() and len(value) == 9

        Rather than:
            if not (value.isdigit() and len(value) == 9)
        """
        cases = [
            ('byr', '2002', True),
            ('byr', '2003', False),
            ('hgt', '60in', True),
            ('hgt', '190cm', True),
            ('hgt', '190in', False),
            ('hgt', '190', False),
            ('hcl', '#123abc', True),
            ('hcl', '#123abz', False),
            ('hcl', '123abc', False),
            ('ecl', 'brn', True),
            ('ecl', 'wat', False),
            ('pid', '000000001', True),
            ('pid', '0123456789', False)
        ]

        for field, value, expected in cases:
            try:
                if field == 'byr':
                    self.solver.validate_between(value, 1920, 2002)
                elif field == 'hgt':
                    self.solver.validate_height(value)
                elif field == 'hcl':
                    self.solver.validate_hair(value)
                elif field == 'ecl':
                    self.solver.validate_eye(value)
                elif field == 'pid':
                    self.solver.validate_pid(value)
                result = True
            except InvalidPassport:
                result = False

            assert result == expected, (field, value, expected)

    def test_passport_validators(self, passport):
        self.solver.validate_presence(passport)
        self.solver.validate_between(passport['byr'], 1920, 2002)
        self.solver.validate_between(passport['iyr'], 2010, 2020)
        self.solver.validate_between(passport['eyr'], 2020, 2030)
        self.solver.validate_height(passport['hgt'])
        self.solver.validate_hair(passport['hcl'])
        self.solver.validate_eye(passport['ecl'])
        self.solver.validate_pid(passport['pid'])


#
# Main
#
TestSuite.run()
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
