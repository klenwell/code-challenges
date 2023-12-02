"""
Advent of Code 2023 - Day 2
https://adventofcode.com/2023/day/2
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class CubeBag:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class CubeGame:
    def __init__(self, input):
        self.input = input

    @property
    def id(self):
        game_id, _ = self.input.split(':')
        _, id = game_id.strip().split(' ')
        return int(id)

    @property
    def grabs(self):
        _, grab_records = self.input.split(':')
        return [CubeGrab(record) for record in grab_records.split(';')]

    def is_possible(self, bag):
        for grab in self.grabs:
            if not grab.is_possible(bag):
                return False
        return True

    def fewest_possible_cubes(self):
        red = max([grab.red for grab in self.grabs])
        blue = max([grab.blue for grab in self.grabs])
        green = max([grab.green for grab in self.grabs])
        return CubeGrab(f'{red} red, {green} green, {blue} blue')


class CubeGrab:
    def __init__(self, record):
        self.record = record
        self.red = 0
        self.green = 0
        self.blue = 0
        self.count_cubes(record)

    @property
    def power(self):
        return self.red * self.green * self.blue

    def count_cubes(self, record):
        cube_counts = [cube_count.strip() for cube_count in record.split(',')]
        for cube_count in cube_counts:
            count, color = cube_count.split(' ')
            setattr(self, color, int(count))

    def is_possible(self, bag):
        return all([self.red <= bag.red, self.green <= bag.green, self.blue <= bag.blue])

    def __repr__(self):
        return f"<Grab red={self.red} green={self.green} blue={self.blue}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-02.txt')

    TEST_INPUT = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

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

        bag = CubeBag(12, 13, 14)
        sum = 0

        for game_input in input.split("\n"):
            game = CubeGame(game_input)

            if game.is_possible(bag):
                sum += game.id

        return sum

    @property
    def second(self):
        input = self.file_input
        sum = 0

        for game_input in input.split("\n"):
            game = CubeGame(game_input)
            grab = game.fewest_possible_cubes()
            sum += grab.power

        return sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT

        bag = CubeBag(12, 13, 14)
        sum = 0

        for game_input in input.split("\n"):
            game = CubeGame(game_input)

            if game.is_possible(bag):
                sum += game.id

        assert sum == 8, sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT

        sum = 0

        for game_input in input.split("\n"):
            game = CubeGame(game_input)
            grab = game.fewest_possible_cubes()
            sum += grab.power

        assert sum == 2286, sum
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
