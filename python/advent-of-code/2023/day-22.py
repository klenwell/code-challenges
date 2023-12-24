"""
Advent of Code 2023 - Day 22
https://adventofcode.com/2023/day/22
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class BrickStack:
    @staticmethod
    def from_snapshot(snapshot):
        bricks = []
        lines = snapshot.strip().split('\n')
        for line in lines:
            left, right = line.split('~')
            pt1 = [int(d) for d in left.strip().split(',')]
            pt2 = [int(d) for d in right.strip().split(',')]
            brick = Brick(pt1, pt2)
            bricks.append(brick)
        return BrickStack(bricks)

    def __init__(self, bricks):
        self.bricks = list(bricks)
        self.floors = self.set_floors()

    def reset(self):
        for brick in self.bricks:
            brick.reset()
        self.floors = self.set_floors()
        return self

    def freeze_bricks(self):
        for brick in self.bricks:
            brick.freeze()
        return self

    @cached_property
    def jenga_sum(self):
        sum = 0

        self.drop_bricks()
        self.freeze_bricks()
        expendable_bricks = self.disintegrate_bricks()

        for brick in self.bricks:
            if brick in expendable_bricks:
                continue
            dropped_bricks = self.drop_bricks()
            sum += dropped_bricks
            print('jenga pull', brick, dropped_bricks, sum)
            self.reset()

        return sum

    def set_floors(self):
        floors = {}

        min_x = min([b.min_x for b in self.bricks])
        max_y = max([b.max_x for b in self.bricks])
        min_y = min([b.min_y for b in self.bricks])
        max_y = max([b.max_y for b in self.bricks])

        for x in range(min_x, max_y + 1):
            for y in range(min_y, max_y + 1):
                floors[(x, y)] = 0
        return floors

    @cached_property
    def expendable_bricks(self):
        self.drop_bricks()
        expendable_bricks = self.disintegrate_bricks()
        return len(expendable_bricks)

    @property
    def brick_count(self):
        return len(self.bricks)

    def drop_bricks(self):
        dropped_bricks = 0
        max_z = max([b.min_z for b in self.bricks])

        for level in range(1, max_z + 1):
            bricks = [b for b in self.bricks if b.min_z == level]
            print(f"dropping level {level}: {len(bricks)} bricks", 100)

            for brick in bricks:
                # Find floor
                old_floor = brick.min_z
                new_floor = max([self.floors[pt] for pt in brick.xy_pts]) + 1
                print(f"move {brick.xy_pts} from floor {old_floor} to {new_floor}")
                brick.set_min_z(new_floor)

                if old_floor != new_floor:
                    dropped_bricks += 1

                # Set new floor for each point
                for pt in brick.xy_pts:
                    old_z = self.floors[pt]
                    new_z = brick.max_z
                    if new_z > old_z:
                        self.floors[pt] = new_z

        return dropped_bricks

    def slow_drop_bricks(self):
        # Sort bricks by min_z asc
        sorted_bricks = sorted(self.bricks, key=lambda b: b.min_z)

        for n, brick in enumerate(sorted_bricks):
            y1 = brick.min_z
            while self.can_drop(brick):
                brick = brick.drop()
            info(f"dropped brick {n} {brick} from y={y1} to y={brick.min_z}", 100)

        return self

    def disintegrate_bricks(self):
        disintegrated_bricks = []

        # Sort bricks by max_z asc
        sorted_bricks = sorted(self.bricks, key=lambda b: b.max_z)

        for n, brick in enumerate(sorted_bricks):
            info(f"testing brick {n} {brick}", 100)
            if self.brick_is_expendable(brick):
                disintegrated_bricks.append(brick)

        # return stack
        #print('expendable', disintegrated_bricks)
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
        dropped_brick = brick.clone()
        dropped_brick = dropped_brick.drop()
        z_level = dropped_brick.min_z

        # Was brick already at ground level?
        if z_level < 1:
            return False

        # Does it collide with any bricks in stack in next level?
        bricks_below = [b for b in self.bricks if b.max_z == z_level]

        for brick_below in bricks_below:
            if dropped_brick.collides(brick_below):
                #print('collision', dropped_brick, brick_below)
                return False
        return True


class Brick:
    def __init__(self, end_pt1, end_pt2):
        self.end_pt1 = tuple(end_pt1)
        self.end_pt2 = tuple(end_pt2)
        self.pts = self.extract_pts()

    def freeze(self):
        self.original_end_pt1 = self.end_pt1
        self.original_end_pt2 = self.end_pt2
        self.pts = self.extract_pts()

    def reset(self):
        self.end_pt1 = self.original_end_pt1
        self.end_pt2 = self.original_end_pt2
        self.pts = self.extract_pts()

    @cached_property
    def xy_pts(self):
        pts = []
        min_x, max_x = sorted([self.end_pt1[0], self.end_pt2[0]])
        min_y, max_y = sorted([self.end_pt1[1], self.end_pt2[1]])
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                pt = (x, y)
                pts.append(pt)
        return pts


    def extract_pts(self):
        pts = []
        min_z, max_z = sorted([self.end_pt1[2], self.end_pt2[2]])
        for x, y in self.xy_pts:
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

    @cached_property
    def min_x(self):
        return min([self.end_pt1[0], self.end_pt2[0]])

    @cached_property
    def max_x(self):
        return max([self.end_pt1[0], self.end_pt2[0]])

    @cached_property
    def min_y(self):
        return min([self.end_pt1[1], self.end_pt2[1]])

    @cached_property
    def max_y(self):
        return max([self.end_pt1[1], self.end_pt2[1]])

    def set_min_z(self, z):
        x1, y1, z1 = self.end_pt1
        x2, y2, z2 = self.end_pt2
        min_z = min(z1, z2)
        dz = min_z - z
        self.end_pt1 = (x1, y1, z1-dz)
        self.end_pt2 = (x2, y2, z2-dz)
        self.pts = self.extract_pts()
        return self

    def drop(self):
        #print('drop', self)
        x1, y1, z1 = self.end_pt1
        x2, y2, z2 = self.end_pt2
        self.end_pt1 = (x1, y1, z1-1)
        self.end_pt2 = (x2, y2, z2-1)
        self.pts = self.extract_pts()
        return self

    def clone(self):
        clone = Brick(self.end_pt1, self.end_pt2)
        return clone

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
        stack = BrickStack.from_snapshot(input)

        assert stack.brick_count == 1205, stack.brick_count
        assert stack.expendable_bricks > 152, stack.expendable_bricks

        return stack.expendable_bricks

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
        stack = BrickStack.from_snapshot(input)

        assert stack.jenga_sum == 7, stack.jenga_sum
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
