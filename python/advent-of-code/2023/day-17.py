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

from models.day_17.route_finder import RouteFinder, N, S, E, W
from models.day_17.route import Route


class UltraRouteFinder(RouteFinder):
    def find_coolest_route(self, start_pt):
        t0 = time.time()

        # Use Dijkstra
        # Because you already start in the top-left block, you don't incur that block's heat loss
        parent_route = None
        hot_path = [HotSpot(self.start_pt, 0)]
        first_route = UltraRoute(parent_route, hot_path)
        open_routes = [first_route]
        route_links = {first_route: None}
        route_costs = {first_route.pt_key: first_route.total_cost}
        possible_routes = 0
        touched_routes = 0

        while open_routes:
            tt = time.time() - t0

            route = heappop(open_routes)
            info(f"touched {touched_routes} of {possible_routes} open={len(open_routes)} {route.end_pt}->{self.end_pt} {route} {tt}", 1000)

            for next_route in self.possible_moves(route):
                possible_routes += 1
                # Cost of next move
                lowest_route_cost = route_costs.get(next_route.pt_key, 100000)

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
        print(end_costs)
        print(coolest_route)
        #breakpoint()
        return coolest_route

    def possible_moves(self, route):
        next_routes = []
        min_steps = 4
        max_steps = 10

        for dx, dy in (N, S, E, W):
            next_pt = (route.x + dx, route.y + dy)
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

            #print('fill', (dx, dy), fill_pts_are_valid, hot_path)
            if not fill_pts_are_valid:
                continue

            for n in range(min_steps, max_steps+1):
                rx = dx * n
                ry = dy * n
                next_pt = (route.x + rx, route.y + ry)
                cost = self.grid.get(next_pt, 1000000)
                hot_spot = HotSpot(next_pt, cost)
                hot_path.append(hot_spot)
                next_route = UltraRoute(route, hot_path)

                if self.is_possible_move(next_route):
                    #print(hot_path, next_route)
                    next_routes.append(next_route)

        return next_routes

    def is_possible_move(self, next_route):
        # Must be on grid
        if next_route.end_pt not in self.pts:
            return False

        # Once an ultra crucible starts moving in a direction, it needs to move a minimum of
        # four blocks in that direction
        if not self.route_moves_n_steps_in_same_direction(next_route, 4):
            #print('too short')
            return False

        # an ultra crucible can move a maximum of ten consecutive blocks without turning
        if self.route_moves_n_steps_in_same_direction(next_route, 11):
            #print('too far')
            return False

        return True

    def route_moves_n_steps_in_same_direction(self, route, n):
        return route.last_n_steps_in_same_direction(n)
        nx, ny = next_pt
        dx = nx - route.x
        dy = ny - route.y
        approach = (dx, dy)
        return route.last_n_steps_in_same_direction(n-1) and approach == route.approach


class UltraRoute(Route):
    def __init__(self, parent, hot_path):
        self.parent = parent
        self.hot_path = sorted(hot_path, key=lambda hp: hp.pt)
        self.x, self.y = hot_path[-1].pt
        self.pt_cost = hot_path[-1].heat

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
    def pt_key(self):
        pts = tuple([h.pt for h in self.hot_path])
        return (self.end_pt, pts)


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


MAX_TIME = 60 * 5


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
        input = self.file_input
        router = UltraRouteFinder(input)
        return router.minimum_heat_loss

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
        assert not route3.last_three_steps_in_same_direction, route3
        assert route4.last_three_steps_in_same_direction, route4
        assert not router.route_moves_four_steps_in_same_direction(route3, (3,0))
        assert router.route_moves_four_steps_in_same_direction(route4, (4,0))
        assert router.route_reverses_direction(route4, (2,0))
        assert not router.route_reverses_direction(route4, (4,0))

        assert router.minimum_heat_loss == 102, router.minimum_heat_loss
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        router = UltraRouteFinder(input)

        route1 = Route(None, (0,0), 1)
        route2 = Route(route1, (1,0), 2)
        route3 = Route(route2, (2,0), 3)
        route4 = Route(route3, (3,0), 4)
        assert route4.last_n_steps_in_same_direction(2), route4
        assert route4.last_n_steps_in_same_direction(3), route4
        assert not route4.last_n_steps_in_same_direction(4), route4
        assert router.route_moves_n_steps_in_same_direction(route4, 3)
        assert not router.route_moves_n_steps_in_same_direction(route4, 4)


        assert router.minimum_heat_loss == 94, router.minimum_heat_loss
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
        #print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
