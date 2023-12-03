"""
Advent of Code 2023 - Day 3
https://adventofcode.com/2023/day/3
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid


class EngineSchematic(Grid):
    @cached_property
    def sum(self):
        return sum([n.value for n in self.part_numbers])

    @cached_property
    def gear_sum(self):
        return sum([gear.ratio for gear in self.gears])

    @property
    def part_numbers(self):
        return [number for number in self.numbers if number.is_adjacent_to_symbol()]

    @cached_property
    def part_number_pt_map(self):
        pt_map = {}
        for part_number in self.part_numbers:
            for pt in part_number.pts:
                pt_map[pt] = part_number
        return pt_map

    @cached_property
    def part_number_pts(self):
        return self.part_number_pt_map.keys()

    @property
    def numbers(self):
        numbers = []

        for y, row in enumerate(self.rows):
            in_digit = False
            for x, value in enumerate(row):
                pt = (x, y)
                if value.isdigit():
                    if in_digit == False:
                        in_digit = True
                        number = SchematicNumber(pt, self)
                        numbers.append(number)
                    else:
                        number.append_digit(x)
                else:
                    if in_digit == True:
                        in_digit = False
        return numbers

    @property
    def star_pts(self):
        pts = []
        for pt in self.pts:
            value = self.grid[pt]
            if value == '*':
                pts.append(pt)
        return pts

    @property
    def gears(self):
        gears = []
        for pt in self.star_pts:
            gear = SchematicGear(pt, self)
            if gear.is_valid():
                gears.append(gear)
        return gears


class SchematicGear:
    def __init__(self, pt, schematic):
        self.pt = pt
        self.x = pt[0]
        self.y = pt[1]
        self.schematic = schematic
        self.part_numbers

    @property
    def grid(self):
        return self.schematic.grid

    @property
    def part_numbers(self):
        part_numbers = []
        neighbors = self.schematic.neighbors(self.pt)
        for npt in neighbors:
            if npt in self.schematic.part_number_pts:
                part_number = self.schematic.part_number_pt_map[npt]
                part_numbers.append(part_number)
        return set(part_numbers)

    @property
    def ratio(self):
        number1, number2 = self.part_numbers
        return number1.value * number2.value

    def is_valid(self):
        return len(self.part_numbers) == 2


class SchematicNumber:
    def __init__(self, pt, schematic):
        self.x = pt[0]
        self.y = pt[1]
        self.xs = [self.x]
        self.schematic = schematic

    @property
    def grid(self):
        return self.schematic.grid

    @property
    def value(self):
        digits = []
        for x in self.xs:
            pt = (x, self.y)
            digits.append(self.grid[pt])
        return int(''.join(digits))

    @property
    def pts(self):
        pts = []
        for x in self.xs:
            pt = (x, self.y)
            pts.append(pt)
        return pts

    def append_digit(self, x):
        self.xs.append(x)

    def is_adjacent_to_symbol(self):
        for x in self.xs:
            pt = (x, self.y)
            for npt in self.schematic.neighbors(pt):
                if self.is_symbol(npt):
                    return True
        return False

    def is_symbol(self, pt):
        value = self.grid[pt]
        if value == '.':
            return False
        if value.isdigit():
            return False
        return True



class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')

    TEST_INPUT = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        schematic = EngineSchematic(input)
        return schematic.sum

    @property
    def second(self):
        input = self.file_input
        schematic = EngineSchematic(input)
        return schematic.gear_sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        schematic = EngineSchematic(input)
        assert schematic.sum == 4361, schematic.sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        schematic = EngineSchematic(input)
        assert schematic.gear_sum == 467835, schematic.gear_sum
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
