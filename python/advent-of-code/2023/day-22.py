"""
Advent of Code 2023 - Day 22
https://adventofcode.com/2023/day/22
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class BrickStack:
    @staticmethod
    def from_snapshot(snapshot):
        bricks = []
        lines = snapshot.strip().split('\n')
        for line in lines:
            left, right = line.split('~')
            pt1 = [int(d) for d in left.strip() if d.isdigit()]
            pt2 = [int(d) for d in right.strip() if d.isdigit()]
            brick = Brick(pt1, pt2)
            bricks.append(brick)
        return BrickStack(bricks)

    def __init__(self, bricks):
        self.bricks = list(bricks)

    @cached_property
    def expendable_bricks(self):
        stack = self.drop_bricks()
        expendable_bricks = stack.disintegrate_bricks()
        return len(expendable_bricks)

    @property
    def brick_count(self):
        return len(self.bricks)

    def drop_bricks(self):
        dropped = []

        # Sort bricks by min_z asc
        sorted_bricks = sorted(self.bricks, key=lambda b: b.max_z)

        for brick in sorted_bricks:
            y1 = brick.max_z
            #print('falling', brick)
            while self.can_drop(brick):
                brick = brick.drop()
            dropped.append(brick)
            print(f"{brick} from y={y1} to y={brick.max_z}")
        return BrickStack(dropped)

    def disintegrate_bricks(self):
        disintegrated_bricks = []

        # Sort bricks by max_z asc
        sorted_bricks = sorted(self.bricks, key=lambda b: b.max_z)

        for brick in sorted_bricks:
            if self.brick_is_expendable(brick):
                disintegrated_bricks.append(brick)

        # return stack
        print('expendable', disintegrated_bricks)
        return disintegrated_bricks

    def brick_is_expendable(self, brick):
        # Remove brick temporarily to test
        self.bricks.remove(brick)

        # Do bricks above stay stable?
        level_above = brick.max_z + 1
        level_above_remains_stable = self.is_level_stable(level_above)

        # Restore brick
        self.bricks.append(brick)

        return level_above_remains_stable

    def is_level_stable(self, z_level):
        bricks_above = [b for b in self.bricks if b.min_z == z_level]
        for brick_above in bricks_above:
            if self.can_drop(brick_above):
               return False
        return True

    def can_drop(self, brick):
        # Drop brick
        dropped_brick = brick.drop()
        z_level = dropped_brick.min_z

        # Was brick already at ground level?
        if z_level < 1:
            return False

        # Does it collide with any bricks in stack in next level?
        bricks_below = [b for b in self.bricks if b.max_z == z_level]

        for brick_below in bricks_below:
            if dropped_brick.collides(brick_below):
                return False
        return True


class Brick:
    def __init__(self, end_pt1, end_pt2):
        self.end_pt1 = tuple(end_pt1)
        self.end_pt2 = tuple(end_pt2)

    @cached_property
    def pts(self):
        pts = []
        min_x, max_x = sorted([self.end_pt1[0], self.end_pt2[0]])
        min_y, max_y = sorted([self.end_pt1[1], self.end_pt2[1]])
        min_z, max_z = sorted([self.end_pt1[2], self.end_pt2[2]])

        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for z in range(min_z, max_z+1):
                    pt = (x, y, z)
                    pts.append(pt)
        return pts

    @property
    def min_z(self):
        return min([z for _, _, z in self.pts])

    @property
    def max_z(self):
        return max([z for _, _, z in self.pts])

    def drop(self):
        x1, y1, z1 = self.end_pt1
        x2, y2, z2 = self.end_pt2
        return Brick((x1, y1, z1-1), (x2, y2, z2-1))

    def collides(self, other):
        common_pts = set(self.pts).intersection(set(other.pts))
        return len(common_pts) > 0

    def __repr__(self):
        return f"<Brick {self.end_pt1}->{self.end_pt2} pts={len(self.pts)}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-22.txt')

    TEST_INPUT = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        stack = BrickStack.from_snapshot(input)

        assert len(stack.bricks) == 7, stack.bricks
        print(stack.bricks[0], stack.bricks[0].pts)

        assert stack.expendable_bricks == 5, stack.expendable_bricks
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
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
