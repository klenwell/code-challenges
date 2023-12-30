"""
Advent of Code 2023 - Day 17
https://adventofcode.com/2023/day/17

Two approaches. Two failures. I think the problem is in my "at most three blocks" logic.
Look at the example and you'll see that this mean you can sometime occupy 4 consecutive
points in a row or column.
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid, info

from heapq import heappush, heappop
from functools import total_ordering
import time


N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)
MAX_TIME = 60 * 5


class RouteFinder(Grid):
    def __init__(self, input):
        self.heat_index = {}
        super().__init__(input)

    @cached_property
    def start_pt(self):
        return (0, 0)

    @cached_property
    def end_pt(self):
        return (self.max_x, self.max_y)

    @cached_property
    def minimum_heat_loss(self):
        route = self.find_coolest_route(self.start_pt)
        return route.total_cost

    def find_coolest_route(self, start_pt):
        t0 = time.time()

        # Use Dijkstra
        # Because you already start in the top-left block, you don't incur that block's heat loss
        parent_route = None
        first_route = Route(parent_route, self.start_pt, 0)
        open_routes = [first_route]
        route_links = {first_route: None}
        route_costs = {first_route.pt_key: first_route.total_cost}
        possible_routes = 0
        touched_routes = 0

        while open_routes:
            tt = time.time() - t0

            route = heappop(open_routes)
            info(f"touched {touched_routes} of {possible_routes} open={len(open_routes)} {route.end_pt}->{self.end_pt} {route} {tt}", 10000)

            for next_route in self.possible_moves(route):
                possible_routes += 1
                # Cost of next move
                #next_route_cost = route_costs[route.pt_key] + next_route.pt_cost
                #print('compare costs', next_route_cost, next_route.total_cost)
                lowest_route_cost = route_costs.get(next_route.pt_key, 100000)

                if route.end_pt in [(10,10), (35,35), (70,70), (105,105), (125,125)]:
                    print((route.end_pt, next_route.end_pt,
                           next_route.total_cost < lowest_route_cost, (next_route.total_cost, lowest_route_cost),
                           next_route))

                # Update costs index for this move if value is lower
                if next_route.total_cost < lowest_route_cost:
                    touched_routes += 1
                    route_costs[next_route.pt_key] = next_route.total_cost
                    heappush(open_routes, next_route)
                    route_links[next_route] = route

            # if tt > MAX_TIME:
            #     breakpoint()
            #     raise Exception('Too long!')

        end_costs = [(pt, cost) for (pt, _), cost in route_costs.items() if pt == self.end_pt]
        end_routes = [route for route in route_links.keys() if route.end_pt == self.end_pt]
        coolest_route = sorted(end_routes, key=lambda r:r.total_cost)[0]
        #print(route_links)
        print(end_routes)
        print(end_costs)
        return coolest_route

    def possible_moves(self, route):
        next_routes = []

        for dx, dy in (N, S, E, W):
            next_pt = (route.x + dx, route.y + dy)
            if self.is_possible_move(route, next_pt):
                next_route = Route(route, next_pt, self.grid[next_pt])
                next_routes.append(next_route)

        return next_routes

    def is_possible_move(self, route, next_pt):
        # Must be on grid
        if next_pt not in self.pts:
            return False

        if self.route_moves_four_steps_in_same_direction(route, next_pt):
            return False

        if self.route_reverses_direction(route, next_pt):
            return False

        return True

    def route_moves_four_steps_in_same_direction(self, route, next_pt):
        # Because it is difficult to keep the top-heavy crucible going in a straight line
        # for very long, it can move at most three blocks in a single direction before
        # it must turn 90 degrees left or right.
        nx, ny = next_pt
        dx = nx - route.x
        dy = ny - route.y
        approach = (dx, dy)
        #print(route, next_pt, route.last_three_steps_in_same_direction, approach == route.approach)
        return route.last_three_steps_in_same_direction and approach == route.approach

    def route_reverses_direction(self, route, next_pt):
        # The crucible also can't reverse direction; after entering each city block, it
        # may only turn left, continue straight, or turn right.
        return route.prev_pt and next_pt == route.prev_pt


@total_ordering
class Route:
    def __init__(self, parent, end_pt, pt_cost):
        self.parent = parent
        self.x, self.y = end_pt
        self.pt_cost = int(pt_cost)

    @cached_property
    def pt_key(self):
        #return (self.end_pt, self.last_three_steps[-3:])
        return (self.end_pt, self.last_three_steps)

    @cached_property
    def approach(self):
        if not self.parent:
            return None

        dx = self.x - self.parent.x
        dy = self.y - self.parent.y
        return (dx, dy)

    @cached_property
    def end_pt(self):
        return (self.x, self.y)

    @cached_property
    def total_cost(self):
        if not self.parent:
            return self.pt_cost
        return self.parent.total_cost + self.pt_cost

    @cached_property
    def pts(self):
        if not self.parent:
            return [self.end_pt]
        return self.parent.pts + [self.end_pt]

    @cached_property
    def prev_pt(self):
        if not self.parent:
            return None
        return self.parent.end_pt

    @cached_property
    def last_three_steps(self):
        return tuple(self.pts[-4:])

    @cached_property
    def last_three_steps_in_same_direction(self):
        if len(self.last_three_steps) < 4:
            return False

        last_xs = set()
        last_ys = set()

        for x, y in self.last_three_steps:
            last_xs.add(x)
            last_ys.add(y)

        return len(last_xs) == 1 or len(last_ys) == 1

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __repr__(self):
        return f"<Route pt_key={self.pt_key} steps={len(self.pts)} total_cost={self.total_cost}>"


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

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        router = RouteFinder(input)
        answer = router.minimum_heat_loss
        assert answer < 772, answer
        return answer

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        router = RouteFinder(input)

        assert len(router.rows) == 13, len(router.rows)
        assert len(router.pts) == 13 * 13, len(router.pts)
        assert router.max_y == 12, router.max_y

        route1 = Route(None, (0,0), 1)
        route2 = Route(route1, (1,0), 2)
        route3 = Route(route2, (2,0), 3)
        route4 = Route(route3, (3,0), 4)
        assert route3.last_three_steps_in_same_direction == False, route3
        assert route4.last_three_steps_in_same_direction == True, route4
        assert not router.route_moves_four_steps_in_same_direction(route3, (3,0))
        assert router.route_moves_four_steps_in_same_direction(route4, (4,0))
        assert router.route_reverses_direction(route4, (2,0))
        assert not router.route_reverses_direction(route4, (4,0))

        assert router.minimum_heat_loss == 102, router.minimum_heat_loss
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
