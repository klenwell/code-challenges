"""
Advent of Code 2023 - Day 17
https://adventofcode.com/2023/day/17

Two approaches. Two failures. I think the problem is in my "at most three blocks" logic.
Look at the example and you'll see that this mean you can sometime occupy 4 consecutive
points in a row or column.
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid

from heapq import heappush, heappop
from functools import total_ordering


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
        route = Route(self.start_pt, self)
        steps = self.fast_dijkstra(route)

        if not steps.get(self.end_pt):
            raise Exception(f"Path not found: {steps}")

        route.path = []
        step = self.end_pt
        while step:
            route.path.insert(0, step)
            step = steps[step]
        return route.heat_loss

    def fast_dijkstra(self, route):
        open_routes = [(0, route)]
        steps = {route.pt: None}
        costs = {route.pt: 0}

        while open_routes:
            cost, route = heappop(open_routes)

            if route.pt == self.end_pt:
                break

            for next_pt in route.options:
                if next_pt in costs:
                    continue

                step_cost = self.grid[next_pt]
                cost = costs[route.pt] + int(step_cost)
                costs[next_pt] = cost
                clone = route.clone()
                clone.move(next_pt)
                heappush(open_routes, (cost, clone))
                steps[next_pt] = route.pt

        return steps

    def path_options(self, pt):
        options = []
        for npt in self.grid.cardinal_neighbors(self.pt):
            if npt in self.path:
                continue

            if self.is_fourth_block_in_row(npt):
                continue

            options.append(npt)

        return options


    def minimize_heat_loss(self):
        best_route = None
        completed_routes = []
        queue = []

        route = Route(self.start_pt, self)
        heappush(queue, route)

        while len(queue) > 0:
            route = heappop(queue)
            print(route, len(queue), route.options, len(completed_routes), best_route)

            for next_pt in route.options:
                clone = route.clone()
                clone.move(next_pt)

                if clone.reached_goal():
                    if not best_route:
                        best_route = clone
                    elif clone.heat_loss < best_route.heat_loss:
                        best_route = clone
                    completed_routes.append(clone)
                elif self.route_is_plausible(clone, best_route):
                    heappush(queue, clone)

        return best_route.heat_loss

    def route_is_plausible(self, clone, best_route):
        if best_route:
            heat_projection = clone.heat_loss + clone.distance_to_end
            if heat_projection >= best_route.heat_loss:
                return False

        heat_index = self.heat_index.get(clone.pt)
        if not heat_index or heat_index >= clone.heat_loss:
            self.heat_index[clone.pt] = clone.heat_loss
        else:
            return False

        return True


@total_ordering
class Route:
    def __init__(self, pt, grid):
        x, y = pt
        self.x = x
        self.y = y
        self.grid = grid
        self.path = []

    @property
    def pt(self):
        return (self.x, self.y)

    @property
    def heat_loss(self):
        loss = 0
        for pt in self.path[1:]:
            value = self.grid.grid[pt]
            loss += int(value)
        return loss

    @property
    def priority(self):
        return (-1 * self.steps, self.heat_loss)

    @property
    def steps(self):
        return len(self.path)

    @property
    def distance_to_end(self):
        fx, fy = self.grid.end_pt
        dx = fx - self.x
        dy = fy - self.y
        return dx + dy

    @property
    def options(self):
        options = []
        for npt in self.grid.cardinal_neighbors(self.pt):
            if npt in self.path:
                continue

            if self.is_fourth_block_in_row(npt):
                continue

            options.append(npt)

        return options

    def move(self, next_pt):
        nx, ny = next_pt
        self.x = nx
        self.y = ny
        self.path.append(self.pt)

    def reached_goal(self):
        return self.pt == self.grid.end_pt

    def is_fourth_block_in_row(self, npt):
        if len(self.path) < 4:
            return False

        start_index = len(self.path) - 4
        last_pts = self.path[start_index:]
        last_xs = [pt[0] for pt in last_pts]
        last_ys = [pt[1] for pt in last_pts]

        last_xs.append(npt[0])
        last_ys.append(npt[1])

        if len(set(last_xs)) == 1:
            return True

        if len(set(last_ys)) == 1:
            return True

        return False

    def clone(self):
        clone = Route(self.pt, self.grid)
        clone.path = list(self.path)
        return clone

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"<Route {id(self)} {self.pt} steps={self.steps} heat_loss={self.heat_loss}>"


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

        heat_loss = router.minimize_heat_loss()
        assert heat_loss == 102, heat_loss
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
