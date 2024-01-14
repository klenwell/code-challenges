"""
Advent of Code 2023 - Day 18
https://adventofcode.com/2023/day/18
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info

from models.day_18.blockcraft import LavaPit, DIRS
from models.day_18.parcel import Parcel
from models.day_18 import polygon as poly


class ParceledLavaPit:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def instructions(self):
        instructions = []
        lines = self.input.split("\n")
        for line in lines:
            dir, size, code = line.strip().split()
            rgb = code[2:-1]
            instruction = (dir, int(size), rgb)
            instructions.append(instruction)
        return instructions

    @cached_property
    def pts(self):
        pts = [(0, 0)]
        for dir, size, _ in self.instructions:
            pt = self.instruction_to_next_pt(pts[-1], dir, size)
            pts.append(pt)
        return pts

    def instruction_to_next_pt(self, previous_pt, dir, distance):
        dx, dy = DIRS[dir]
        px, py = previous_pt
        x = px + (dx * distance)
        y = py + (dy * distance)
        pt = (x, y)
        return pt

    @cached_property
    def cubic_meters(self):
        """Go column by column, row by row for each parcel and compute area. Because parcels
        will overlap at the borders, it's necessary to do some adjustments to each parcel area
        depending on neighbors.
        """
        area = 0
        for key, parcel in self.parcel_grid.items():
            row_num, col_num = key
            net_parcel_area = 0
            info(f"({key}) {parcel}", 10000)

            # Only count those parcels that are inside the pit perimeter
            if not self.is_interior_parcel(parcel):
                continue

            # Find neighbors to do area adjustments
            left_neighbor = self.parcel_grid.get((row_num, col_num-1))
            upper_neighbor = self.parcel_grid.get((row_num-1, col_num))
            upper_right_neighbor = self.parcel_grid.get((row_num-1, col_num+1))

            # Compute area and start making adjustments
            net_parcel_area = parcel.area

            subtract_left_edge = left_neighbor and self.is_interior_parcel(left_neighbor)
            subtract_upper_edge = upper_neighbor and self.is_interior_parcel(upper_neighbor)
            subtract_upper_right_corner = not subtract_upper_edge and upper_right_neighbor and \
                self.is_interior_parcel(upper_right_neighbor)
            add_back_upper_left_corner = subtract_left_edge and subtract_upper_edge

            if subtract_left_edge:
                net_parcel_area -= parcel.height
            if subtract_upper_edge:
                net_parcel_area -= parcel.width
            if subtract_upper_right_corner:
                net_parcel_area -= 1
            if add_back_upper_left_corner:
                net_parcel_area += 1

            # Update running area total
            area += net_parcel_area
        return area

    @cached_property
    def xs(self):
        return sorted(list(set([x for x, _ in self.pts])))

    @cached_property
    def ys(self):
        return sorted(list(set([y for _, y in self.pts])))

    @cached_property
    def parcel_grid(self):
        parcels = {}
        for row_num, y in enumerate(self.ys[:-1]):
            for col_num, x in enumerate(self.xs[:-1]):
                next_x = self.xs[col_num+1]
                next_y = self.ys[row_num+1]
                pts = [
                    (x, y),
                    (next_x, y),
                    (next_x, next_y),
                    (x, next_y)
                ]
                parcel = Parcel(pts)
                parcels[(row_num, col_num)] = parcel
        return parcels

    @cached_property
    def parcels(self):
        parcels = []
        for key in sorted(list(self.parcel_grid.keys())):
            parcel = self.parcel_grid[key]
            parcels.append(parcel)
        return parcels

    @cached_property
    def horizontal_edges(self):
        edges = []
        for n, pt in enumerate(self.pts[:-1]):
            next_pt = self.pts[n+1]
            _, y = pt
            _, ny = next_pt
            if y == ny:
                edge = (pt, next_pt)
                edges.append(edge)
        return edges

    @cached_property
    def vertical_edges(self):
        edges = []
        for n, pt in enumerate(self.pts[:-1]):
            next_pt = self.pts[n+1]
            x, _ = pt
            nx, _ = next_pt
            if x == nx:
                edge = (pt, next_pt)
                edges.append(edge)
        return edges

    def is_interior_parcel(self, parcel):
        def is_odd(num):
            return num % 2 == 1

        edges_above = poly.count_edges_above_pt(self.horizontal_edges, parcel.mid_pt)
        if not is_odd(edges_above):
            return False

        edges_to_left = poly.count_edges_left_of_pt(self.vertical_edges, parcel.mid_pt)
        if not is_odd(edges_to_left):
            return False

        # These checks below turned out not to be needed.
        # edges_below = poly.count_edges_below_pt(self.horizontal_edges, parcel.mid_pt)
        # if not is_odd(edges_below):
        #     return False

        # edges_to_right = poly.count_edges_right_of_pt(self.vertical_edges, parcel.mid_pt)
        # if not is_odd(edges_to_right):
        #     return False

        return True


class ParceledLargePit(ParceledLavaPit):
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def instructions(self):
        instructions = []
        lines = self.input.split("\n")
        for line in lines:
            dir, size, code = line.strip().split()
            rgb = code[2:-1]
            instruction = (dir, int(size), rgb)
            instructions.append(instruction)
        return instructions

    @cached_property
    def pts(self):
        pts = [(0, 0)]
        for _, _, rgb in self.instructions:
            pt = self.rgb_to_next_pt(pts[-1], rgb)
            pts.append(pt)
        return pts

    def rgb_to_next_pt(self, previous_pt, rgb):
        dir_map = list('RDLU')

        hex = rgb[:-1]
        dir_code = int(rgb[-1:])

        dir = dir_map[dir_code]
        dx, dy = DIRS[dir]

        # https://stackoverflow.com/a/209550/1093087
        distance = int(hex, 16)

        px, py = previous_pt
        x = px + (dx * distance)
        y = py + (dy * distance)
        pt = (x, y)
        return pt


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-18.txt')

    TEST_INPUT = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        pit = ParceledLavaPit(input)
        assert pit.cubic_meters == 33491
        return pit.cubic_meters

    @property
    def second(self):
        input = self.file_input
        pit = ParceledLargePit(input)
        assert pit.cubic_meters != 98956108013068, pit.cubic_meters
        assert pit.cubic_meters != 98956107977040, pit.cubic_meters
        assert pit.cubic_meters != 87716969654495, pit.cubic_meters
        assert pit.cubic_meters == 87716969654406, pit.cubic_meters
        return pit.cubic_meters

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        pit = LavaPit(input)
        assert pit.cubic_meters == 62, pit.cubic_meters

        pit = ParceledLavaPit(input)
        assert pit.cubic_meters == 62, pit.cubic_meters
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        pit = ParceledLargePit(input)

        def errs(val, expected):
            diff = expected - val
            verb = 'over' if diff < 0 else 'under'
            pct = 100.0 * diff / expected
            return f"got {val} expected {expected} {verb} by {abs(diff)} ({abs(pct)}%)"

        assert pit.cubic_meters == 952408144115, errs(pit.cubic_meters, 952408144115)
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
