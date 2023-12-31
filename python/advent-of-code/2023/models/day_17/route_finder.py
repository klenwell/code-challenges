from functools import cached_property
from common import Grid, info
from heapq import heappush, heappop
import time

from models.day_17.route import Route


N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)


class RouteFinder(Grid):
    def __init__(self, input):
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
        return route.last_three_steps_in_same_direction and approach == route.approach

    def route_reverses_direction(self, route, next_pt):
        # The crucible also can't reverse direction; after entering each city block, it
        # may only turn left, continue straight, or turn right.
        return route.prev_pt and next_pt == route.prev_pt