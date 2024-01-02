"""
Advent of Code 2023 - Day 17
https://adventofcode.com/2023/day/17

Two approaches. Two failures. I think the problem is in my "at most three blocks" logic.
Look at the example and you'll see that this mean you can sometime occupy 4 consecutive
points in a row or column.
"""
from os.path import join as path_join
from functools import cached_property, total_ordering
from common import INPUT_DIR, info, Grid

from heapq import heappush, heappop


N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)


class RouteFinder(Grid):
    def __init__(self, input, min_straight_path, max_straight_path):
        self.min_straight_path = min_straight_path
        self.max_straight_path = max_straight_path
        self.route_key_len = max_straight_path - min_straight_path + 1
        super().__init__(input)

    @cached_property
    def start_pt(self):
        return (0, 0)

    @cached_property
    def end_pt(self):
        return (self.max_x, self.max_y)

    @cached_property
    def minimum_heat_loss(self):
        route = self.find_coolest_route()
        return route.total_cost

    def find_coolest_route(self):
        # Use Dijkstra
        # Because you already start in the top-left block, you don't incur that block's heat loss
        hot_path = [HotSpot(self.start_pt, 0)]
        first_route = Route(None, hot_path, self.route_key_len)
        open_routes = [first_route]
        route_costs = {first_route.pt_key: first_route.total_cost}
        visited_routes = set()
        completed_routes = []

        def already_visit_pt_key(pt_key):
            return pt_key in visited_routes

        while open_routes:
            route = heappop(open_routes)
            visited_routes.add(route.pt_key)
            info(f"open={len(open_routes)} {route.end_pt}->{self.end_pt} {route}", 10000)

            for next_route in self.possible_moves(route):
                # Avoid duplicated
                if already_visit_pt_key(next_route.pt_key):
                    continue

                # Cost of next move
                lowest_route_cost = route_costs.get(next_route.pt_key, 100000)

                # Update costs index for this move if value is lower
                if next_route.total_cost < lowest_route_cost:
                    route_costs[next_route.pt_key] = next_route.total_cost
                    heappush(open_routes, next_route)

                if next_route.end_pt == self.end_pt:
                    completed_routes.append(next_route)

        coolest_route = sorted(completed_routes, key=lambda r: r.total_cost)[0]
        return coolest_route

    def possible_moves(self, route):
        next_routes = []
        min_steps = self.min_straight_path
        max_steps = self.max_straight_path

        for dx, dy in (N, S, E, W):
            next_pt = (route.x + dx, route.y + dy)

            # Filter out moves reversing direction
            if route.prev_pt and next_pt == route.prev_pt:
                continue

            hot_path = []
            fill_pts_are_valid = True

            # fill in steps between current and min_steps
            for n in range(1, min_steps):
                rx = dx * n
                ry = dy * n
                next_pt = (route.x + rx, route.y + ry)
                heat = self.grid.get(next_pt)
                if heat:
                    hot_spot = HotSpot(next_pt, heat)
                    hot_path.append(hot_spot)
                else:
                    fill_pts_are_valid = False
                    break

            if not fill_pts_are_valid:
                continue

            for n in range(min_steps, max_steps+1):
                rx = dx * n
                ry = dy * n
                next_pt = (route.x + rx, route.y + ry)
                cost = self.grid.get(next_pt, 1000000)
                hot_spot = HotSpot(next_pt, cost)
                hot_path.append(hot_spot)
                next_route = Route(route, hot_path, self.route_key_len)

                if self.is_possible_move(next_route):
                    next_routes.append(next_route)

        return next_routes

    def is_possible_move(self, next_route):
        if not self.is_pt_in_grid(next_route.end_pt):
            return False

        if not next_route.last_n_steps_in_same_direction(self.min_straight_path):
            return False

        if next_route.last_n_steps_in_same_direction(self.max_straight_path+1):
            return False

        return True


@total_ordering
class Route:
    def __init__(self, parent, hot_path, key_len):
        self.parent = parent
        self.hot_path = hot_path
        self.key_len = key_len
        self.x, self.y = hot_path[-1].pt
        self.pt_cost = hot_path[-1].heat

    @cached_property
    def pt_key(self):
        # This was a big bottleneck.
        # Thanks to https://advent-of-code.xavd.id/writeups/2023/day/17/ found in solution thread.
        # Making change below cut from over 5 mins to just over 1
        # pts = self.last_n_steps(self.key_len)
        # return (self.end_pt, pts)
        dir = self.approach
        steps_in_row = len(self.hot_path)
        return (self.end_pt, dir, steps_in_row)

    @cached_property
    def total_cost(self):
        return sum([hs.heat for hs in self.hot_spots])

    @cached_property
    def hot_spots(self):
        if not self.parent:
            return self.hot_path
        return self.parent.hot_spots + self.hot_path

    @cached_property
    def pts(self):
        return [h.pt for h in self.hot_spots]

    @cached_property
    def approach(self):
        if not len(self.pts) > 1:
            return None

        last_pt = self.pts[-2]
        lx, ly = last_pt

        dx = self.x - lx
        dy = self.y - ly
        return (dx, dy)

    @cached_property
    def end_pt(self):
        return (self.x, self.y)

    @cached_property
    def prev_pt(self):
        if not self.parent:
            return None
        return self.parent.end_pt

    def reverses_direction(self):
        if not self.parent:
            return False
        return self.prev_pt and self.end_pt

    def last_n_steps(self, n):
        start = -1 * n
        return tuple(self.pts[start:])

    def last_n_steps_in_same_direction(self, n):
        last_n_steps = self.last_n_steps(n+1)

        if len(last_n_steps) < n+1:
            return False

        last_xs = set()
        last_ys = set()

        for x, y in last_n_steps:
            last_xs.add(x)
            last_ys.add(y)

        return len(last_xs) == 1 or len(last_ys) == 1

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __repr__(self):
        return f"<Route pt_key={self.pt_key} steps={len(self.pts)} total_cost={self.total_cost}>"


class HotSpot:
    def __init__(self, pt, heat):
        self.pt = pt
        self.heat = int(heat)

    @cached_property
    def x(self):
        return self.pt[0]

    @cached_property
    def y(self):
        return self.pt[1]

    def __repr__(self):
        return f"<HotSpot {self.pt} heat={self.heat}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-17.txt')

    TEST_INPUT = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

    TEST_INPUT_PART_2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991"""

    #
    # Solutions
    #
    @property
    def first(self):
        min_straight_step, max_straight_steps = 1, 3
        input = self.file_input
        router = RouteFinder(input, min_straight_step, max_straight_steps)
        answer = router.minimum_heat_loss
        assert answer < 772, answer
        assert answer == 758, answer
        return answer

    @property
    def second(self):
        # Once an ultra crucible starts moving in a direction, it needs to move a minimum of
        # four blocks in that direction... an ultra crucible can move a maximum of ten
        # consecutive blocks without turning
        min_straight_step, max_straight_steps = 4, 10
        input = self.file_input
        router = RouteFinder(input, min_straight_step, max_straight_steps)
        answer = router.minimum_heat_loss
        assert answer > 887, answer
        return router.minimum_heat_loss

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        router = RouteFinder(input, 1, 3)
        assert len(router.rows) == 13, len(router.rows)
        assert len(router.pts) == 13 * 13, len(router.pts)
        assert router.max_y == 12, router.max_y
        assert router.route_key_len == 3, router.route_key_len

        route1 = Route(None, [HotSpot((0, 0), 1)], router.route_key_len)
        route2 = Route(route1, [HotSpot((1, 0), 2)], router.route_key_len)
        route3 = Route(route2, [HotSpot((2, 0), 3)], router.route_key_len)
        route4 = Route(route3, [HotSpot((3, 0), 4)], router.route_key_len)
        assert not route3.last_n_steps_in_same_direction(3), route3
        assert route4.last_n_steps_in_same_direction(3), route4

        assert router.minimum_heat_loss == 102, router.minimum_heat_loss
        return 'passed'

    @property
    def test2(self):
        # Test 1
        input = self.TEST_INPUT
        router = RouteFinder(input, 4, 10)
        assert router.minimum_heat_loss == 94, router.minimum_heat_loss

        # Test 2
        input = self.TEST_INPUT_PART_2
        router = RouteFinder(input, 4, 10)
        assert router.minimum_heat_loss == 71, router.minimum_heat_loss

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
