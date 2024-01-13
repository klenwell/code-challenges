"""
Advent of Code 2023 - Day 18
https://adventofcode.com/2023/day/18
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info

#from models.day_18.lava_pit import SmallLavaPit, BigLavaPit
from models.day_18 import polygon as poly


DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}



class ParceledLavaPit:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def xs(self):
        return sorted(list(set([x for x,_ in self.pts])))

    @cached_property
    def ys(self):
        return sorted(list(set([y for _,y in self.pts])))

    @cached_property
    def cubic_meters(self):
        area = 0
        for key, parcel in self.parcel_grid.items():
            row_num, col_num = key

            if not self.is_interior_parcel(parcel):
                continue

            left_neighbor = self.parcel_grid.get((row_num, col_num-1))
            upper_neighbor = self.parcel_grid.get((row_num-1, col_num))
            upper_left_neighbor = self.parcel_grid.get((row_num-1, col_num-1))

            area += parcel.area

            subtract_left_edge = left_neighbor and self.is_interior_parcel(left_neighbor)
            subtract_upper_edge = upper_neighbor and self.is_interior_parcel(upper_neighbor)
            add_back_corner = subtract_left_edge and subtract_upper_edge

            shifted = False

            if subtract_left_edge:
                area -= parcel.height
                shifted = True
            if subtract_upper_edge:
                area -= parcel.width
                shifted = True

            if add_back_corner:
                area += 1

            if not shifted:
                if upper_left_neighbor and self.is_interior_parcel(upper_left_neighbor):
                    print(parcel, upper_left_neighbor)
                    area -= 1
                    breakpoint()
        return area

    def is_interior_parcel(self, parcel):
        info(f"is_interior_parcel {parcel}", 10000)
        def is_odd(num):
            return num % 2 == 1
        edges_above = poly.count_edges_above_pt(self.horizontal_edges, parcel.mid_pt)
        edges_below = poly.count_edges_below_pt(self.horizontal_edges, parcel.mid_pt)
        edges_to_left = poly.count_edges_left_of_pt(self.vertical_edges, parcel.mid_pt)
        edges_to_right = poly.count_edges_right_of_pt(self.vertical_edges, parcel.mid_pt)
        return all([
            is_odd(edges_above),
            is_odd(edges_below),
            is_odd(edges_to_left),
            is_odd(edges_to_right)
        ])

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
        breakpoint()
        return pts

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
                parcel = Parcel(pts, self)
                parcels[(row_num, col_num)] = parcel
                info(parcel, 1000)
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
        print(rgb, dir, distance, pt)
        return pt


class Parcel:
    def __init__(self, pts, pit):
        self.pts = pts
        self.pit = pit

    @property
    def area(self):
        return self.width * self.height

    @property
    def width(self):
        # Edge case: consider box with pts (0,0) -> (4,0) -> (4,4) -> (0,0). Subtracting
        # coordinates gives you 4x4 when it should be 5x5.
        return max(self.xs) - self.min_x + 1

    @property
    def height(self):
        return max(self.ys) - self.min_y + 1

    @property
    def xs(self):
        return [x for x,_ in self.pts]

    @property
    def ys(self):
        return [y for _,y in self.pts]

    @property
    def min_x(self):
        return min(self.xs)

    @property
    def min_y(self):
        return min(self.ys)

    def shift_left(self):
        pts = []
        for x, y in self.pts:
            if x == self.min_x:
                new_pt = (x+1, y)
            else:
                new_pt = (x, y)
            pts.append(new_pt)
        self.pts = pts
        return self

    def shift_down(self):
        pts = []
        for x, y in self.pts:
            if y == self.min_y:
                new_pt = (x, y+1)
            else:
                new_pt = (x, y)
            pts.append(new_pt)
        self.pts = pts
        return self

    @cached_property
    def edges(self):
        edges = []
        pts = self.pts + [self.pts[0]]
        for n, pt in enumerate(pts[:-1]):
            next_pt = pts[n+1]
            min_pt, max_pt = sorted([pt, next_pt])
            edge = (min_pt, max_pt)
            edges.append(edge)
        return edges

    @cached_property
    def area(self):
        # Edge case: consider box with pts (0,0) -> (4,0) -> (4,4) -> (0,0). Subtracting
        # coordinates gives you 4x4 when it should be 5x5.
        width = max(self.xs) - min(self.xs) + 1
        height = max(self.ys) - min(self.ys) + 1
        return width * height

    @cached_property
    def mid_pt(self):
        x = (max(self.xs) + min(self.xs)) // 2
        y = (max(self.ys) + min(self.ys)) // 2
        return (x, y)

    def shares_edge_with(self, other):
        return len(set(self.edges).intersection(set(other.edges))) > 0

    def __repr__(self):
        return f"<Parcel {self.pts} mid_pt={self.mid_pt} area={self.area}>"


class Hole:
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb

    @property
    def pt(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"<Hole {self.pt} rgb={self.rgb}>"


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
        pit = LavaPit(input)
        return pit.cubic_meters

    @property
    def second(self):
        input = self.file_input
        pit = ParceledLavaPit(input)
        #print(len(pit.parcels))
        assert pit.cubic_meters != 98956108013068, pit.cubic_meters
        assert pit.cubic_meters != 98956107977040, pit.cubic_meters
        assert pit.cubic_meters != 87716969654495, pit.cubic_meters
        return pit.cubic_meters

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        pit = LavaPit(input)
        assert pit.cubic_meters == 62, pit.cubic_meters
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        pit = ParceledLavaPit(input)

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
        #print(f"test 1 solution: {self.test1}")
        #print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
