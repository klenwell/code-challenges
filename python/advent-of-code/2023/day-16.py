"""
Advent of Code 2023 - Day 16
https://adventofcode.com/2023/day/16

NOTE: Due to some chicanery with they way Python handles backslashes
(https://stackoverflow.com/q/647769), I find-replaced all the backslashes '\' in the input data
 with 'V'.
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid


NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

global_id = 1


class BeamGrid(Grid):
    def __init__(self, input):
        self.energy_map = {}
        self.beam_log = {}
        self.beam = Beam(-1, 0, EAST)
        super().__init__(input)

    @cached_property
    def energized_tiles(self):
        self.fire_beam_into_grid()
        return len(self.energy_map.keys())

    def fire_beam_into_grid(self):
        beams_queue = [self.beam]

        while len(beams_queue) > 0:
            beam = beams_queue.pop()
            new_beam = self.move_beam(beam)

            if new_beam:
                beams_queue.insert(0, new_beam)

            if beam.log_key in self.beam_log:
                previous_beam = self.beam_log[beam.log_key]
                beam.join(previous_beam)
            elif self.beam_in_grid(beam):
                self.log_beam(beam)
                self.energize_tile(beam.pt)
                beams_queue.insert(0, beam)

    def move_beam(self, beam):
        beam.move()
        tile = self.grid.get(beam.pt)

        # No tile? Off grid.
        if not tile:
            return None

        if self.tile_is_splitter(tile):
            if self.does_splitter_rotate_beam(tile, beam):
                beam.rotate_clockwise()
                new_beam = beam.split()
                return new_beam
        elif self.tile_is_mirror(tile):
            self.bounce_beam_off_mirror(beam, tile)

        return None

    def beam_in_grid(self, beam):
        return beam.pt in self.pts

    def tile_is_splitter(self, tile):
        return tile in ('|', '-')

    def tile_is_mirror(self, tile):
        return tile in ('/', 'V')

    def does_splitter_rotate_beam(self, splitter, beam):
        if splitter == '|':
            return beam.dir in (WEST, EAST)
        else:
            return beam.dir in (NORTH, SOUTH)

    def bounce_beam_off_mirror(self, beam, mirror):
        reflections = {
            '/': {
                NORTH: EAST,
                EAST: NORTH,
                SOUTH: WEST,
                WEST: SOUTH
            },
            'V': {
                NORTH: WEST,
                EAST: SOUTH,
                SOUTH: EAST,
                WEST: NORTH
            }
        }
        beam.dir = reflections[mirror][beam.dir]

    def energize_tile(self, pt):
        if pt in self.energy_map:
            self.energy_map[pt] += 1
        else:
            self.energy_map[pt] = 1

    def log_beam(self, beam):
        if beam.log_key not in self.energy_map:
            self.beam_log[beam.log_key] = beam


class Beam:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.path = [self.pt]

        global global_id
        global_id += 1
        self.id = global_id

    @property
    def pt(self):
        return (self.x, self.y)

    @property
    def log_key(self):
        return (self.x, self.y, self.dir)

    def move(self):
        dx, dy = self.dir
        self.x += dx
        self.y += dy
        self.path.append(self.pt)

    def split(self):
        new_beam = Beam(self.x, self.y, self.dir)
        new_beam.reverse_direction()
        return new_beam

    def join(self, other_beam):
        # Nothing really needs to be done here.
        pass

    def rotate_clockwise(self):
        mappings = {
            NORTH: EAST,
            EAST: SOUTH,
            SOUTH: WEST,
            WEST: NORTH
        }
        self.dir = mappings[self.dir]

    def reverse_direction(self):
        x = self.dir[0] * -1
        y = self.dir[1] * -1
        self.dir = (x, y)

    def __repr__(self):
        dir_mapping = [(NORTH, 'N'), (SOUTH, 'S'), (EAST, 'E'), (WEST, 'W')]
        dir = dict(dir_mapping)[self.dir]
        return f"<Beam id={self.id} step={len(self.path)} {self.pt} dir={dir}>"


class ControlPanel:
    def __init__(self, input):
        self.input = input

    @cached_property
    def starting_pts(self):
        pts = []
        grid = BeamGrid(self.input)

        # North / South
        for x in range(grid.max_x+1):
            top = (x, -1, SOUTH)
            bottom = (x, grid.max_y+1, NORTH)
            pts += [top, bottom]

        # West / East
        for y in range(grid.max_y+1):
            left = (-1, y, EAST)
            right = (grid.max_x+1, y, WEST)
            pts += [left, right]

        return pts

    def maximize_energy(self):
        energy_outputs = []
        print(len(self.starting_pts))

        for x, y, dir in self.starting_pts:
            grid = BeamGrid(self.input)
            grid.beam = Beam(x, y, dir)
            energy_outputs.append(grid.energized_tiles)
            print(len(energy_outputs), (x, y), energy_outputs[-1])

        return max(energy_outputs)


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')

    TEST_INPUT = """\
.|...V....
|.-.V.....
.....|-...
........|.
..........
.........V
..../.VV..
.-.-/..|..
.|....-|.V
..//.|...."""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        grid = BeamGrid(input)
        return grid.energized_tiles

    @property
    def second(self):
        input = self.file_input
        panel = ControlPanel(input)
        max_tiles = panel.maximize_energy()
        return max_tiles

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        grid = BeamGrid(input)

        assert len(grid.pts) == 100, grid
        assert grid.grid[(6,6)] == 'V', grid.grid[(6, 6)]

        assert grid.energized_tiles == 46, grid.energized_tiles
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        panel = ControlPanel(input)
        max_tiles = panel.maximize_energy()
        assert max_tiles == 51, max_tiles
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
