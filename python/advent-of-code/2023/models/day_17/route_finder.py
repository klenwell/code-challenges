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
        first_route = UltraRoute(None, hot_path, self.route_key_len)
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
                next_route = UltraRoute(route, hot_path, self.route_key_len)

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
