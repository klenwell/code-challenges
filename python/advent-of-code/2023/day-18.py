"""
Advent of Code 2023 - Day 18
https://adventofcode.com/2023/day/18
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}


class LavaPit:
    def __init__(self, input):
        self.input = input.strip()
        self.holes = {}

    @cached_property
    def cubic_meters(self):
        self.excavate()
        self.fill()
        return len(self.holes)

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

    def excavate(self):
        hole = Hole(0, 0, None)
        for dir, size, rgb in self.instructions:
            dx, dy = DIRS[dir]
            for n in range(size):
                hole.x += dx
                hole.y += dy
                hole.rgb = rgb
                self.dig_hole(hole)
                info(f"excavating {hole}", 1000)

    def fill(self):
        start_pt = self.find_inner_pt()
        queue = [start_pt]

        while len(queue) > 0:
            x, y = queue.pop()
            hole = Hole(x, y, None)
            self.dig_hole(hole)
            info(f"filling {hole}", 10000)


            for npt in self.neighbors(hole.pt):
                if npt not in self.holes:
                    queue.append(npt)

    def find_inner_pt(self):
        iy = min([y for _,y in self.holes.keys()])
        ix = min([x for x,y in self.holes.keys() if y == iy])


        hole = self.holes.get((ix, iy), False)

        while hole:
            print(hole)
            ix = hole.x + 1
            iy = hole.y + 1
            hole = self.holes.get((ix, iy), False)

        print('start', ix, iy)
        #breakpoint()
        return (ix, iy)

    def neighbors(self, pt):
        x, y = pt
        for dx, dy in DIRS.values():
            yield (x+dx, y+dy)

    def dig_hole(self, hole):
        new_hole = Hole(hole.x, hole.y, hole.rgb)
        self.holes[new_hole.pt] = new_hole


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


class BigLavaPit(LavaPit):
    @cached_property
    def cubic_meters(self):
        area = 0
        for parcel in self.interior_parcels:
            area += parcel.area
        return area - self.overlapping_edges_area

    @cached_property
    def interior_parcels(self):
        return [parcel for parcel in self.parcels if self.contains_parcel(parcel)]

    @cached_property
    def edge_counts(self):
        edge_counts = {}
        pt_counts = {}
        for parcel in self.interior_parcels:
            for edge in parcel.edges:
                if edge in edge_counts:
                    edge_counts[edge] += 1
                else:
                    edge_counts[edge] = 1
        return edge_counts

    @cached_property
    def overlapping_edges(self):
        edges = []
        for edge, count in self.edge_counts.items():
            if count > 1:
                edges.append(edge)
                assert count == 2, f"count for edge > 1 ({count})"
        return edges

    @cached_property
    def overlapping_corners(self):
        pt_counts = {}
        for edge in self.edge_counts.keys():
            pt1, pt2 = edge
            pt1_count = pt_counts.get(pt1, 0)
            pt2_count = pt_counts.get(pt2, 0)
            pt_counts[pt1] = pt1_count + 1
            pt_counts[pt2] = pt2_count + 1
        return pt_counts

    @cached_property
    def overlapping_edges_area(self):
        area = 0
        for edge in self.overlapping_edges:
            (x1, y1), (x2, y2) = edge
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            assert 0 in [dx, dy], (dx, dy)
            area += dx + dy
        overcounted_corners = sum([n-2 for n in self.overlapping_corners.values()]) // 2
        return area + overcounted_corners

    @cached_property
    def parcels(self):
        parcels = []
        for i, x in enumerate(self.xs[:-1]):
            for j, y in enumerate(self.ys[:-1]):
                next_x = self.xs[i+1]
                next_y = self.ys[j+1]
                pts = [
                    (x, y),
                    (next_x, y),
                    (next_x, next_y),
                    (x, next_y)
                ]
                parcel = Parcel(pts)
                parcels.append(parcel)
                info(parcel, 1000)
        return parcels

    @cached_property
    def pts(self):
        pts = [(0, 0)]
        for _, _, rgb in self.instructions:
            pt = self.rgb_to_next_pt(pts[-1], rgb)
            pts.append(pt)
        return pts

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
        #print(rgb, dir, distance)

        px, py = previous_pt
        x = px + (dx * distance)
        y = py + (dy * distance)
        pt = (x, y)
        return pt

    @cached_property
    def xs(self):
        return sorted(list(set([x for x,_ in self.pts])))

    @cached_property
    def ys(self):
        return sorted(list(set([y for _,y in self.pts])))

    def contains_parcel(self, parcel):
        info(f"contains {parcel}", 10000)
        under_top_edge = self.pt_under_top_edge(parcel.mid_pt)
        above_bottom_edge = self.pt_above_bottom_edge(parcel.mid_pt)
        right_of_left_edge = self.pt_right_of_left_edge(parcel.mid_pt)
        left_of_right_edge = self.pt_left_of_right_edge(parcel.mid_pt)
        return all([under_top_edge, above_bottom_edge, right_of_left_edge, left_of_right_edge])

    def pt_under_top_edge(self, pt):
        x, y = pt
        for edge in self.horizontal_edges:
            pt1, pt2 = edge
            e1x, e1y = pt1
            e2x, e2y = pt2
            assert e1y == e2y, edge
            min_x, max_x = sorted([e1x, e2x])
            between_xs = min_x <= x <= max_x
            under_edge = y > e1y
            if between_xs and under_edge:
                return True
        return False

    def pt_above_bottom_edge(self, pt):
        x, y = pt
        for edge in self.horizontal_edges:
            pt1, pt2 = edge
            e1x, e1y = pt1
            e2x, e2y = pt2
            assert e1y == e2y, edge
            min_x, max_x = sorted([e1x, e2x])
            between_xs = min_x <= x <= max_x
            above_edge = y < e1y
            if between_xs and above_edge:
                return True
        return False

    def pt_right_of_left_edge(self, pt):
        x, y = pt
        for edge in self.vertical_edges:
            pt1, pt2 = edge
            e1x, e1y = pt1
            e2x, e2y = pt2
            assert e1x == e2x, edge
            min_y, max_y = sorted([e1y, e2y])
            between_ys = min_y <= y <= max_y
            right_of_edge = x > e1x
            if between_ys and right_of_edge:
                return True
        return False

    def pt_left_of_right_edge(self, pt):
        x, y = pt
        for edge in self.vertical_edges:
            pt1, pt2 = edge
            e1x, e1y = pt1
            e2x, e2y = pt2
            assert e1x == e2x, edge
            min_y, max_y = sorted([e1y, e2y])
            between_ys = min_y <= y <= max_y
            left_of_edge = x < e1x
            if between_ys and left_of_edge:
                return True
        return False


class Parcel:
    def __init__(self, pts):
        self.pts = pts
        self.xs = [x for x,_ in pts]
        self.ys = [y for _,y in pts]

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

    def __repr__(self):
        return f"<Parcel {self.pts} mid_pt={self.mid_pt} area={self.area}>"


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
        pit = BigLavaPit(input)
        print(len(pit.parcels))
        assert pit.cubic_meters != 98956108013068, pit.cubic_meters
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
        pit = BigLavaPit(input)

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
