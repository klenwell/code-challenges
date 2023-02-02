"""
Advent of Code 2015 - Day 09
https://adventofcode.com/2015/day/9
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class SantaRouter:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def input_lines(self):
        return [line for line in self.input.split('\n')]

    @cached_property
    def location_pairs(self):
        pairs = []
        for line in self.input_lines:
            locations, distance = line.split(' = ')
            l1, l2 = locations.split(' to ')
            pair = (l1.strip(), l2.strip(), int(distance.strip()))
            pairs.append(pair)
        return pairs

    @cached_property
    def location_destinations(self):
        mapped = {}
        for l1, l2, _ in self.location_pairs:
            if l1 in mapped:
                mapped[l1].append(l2)
            else:
                mapped[l1] = [l2]

            if l2 in mapped:
                mapped[l2].append(l1)
            else:
                mapped[l2] = [l1]
        return mapped

    @cached_property
    def legs(self):
        pass

    @cached_property
    def leg_distances(self):
        pass

    @property
    def starting_location(self):
        lds = self.location_destinations.items()
        sorted_locations = sorted(lds, key=lambda kv: len(kv[1]))
        return sorted_locations[0][0]

    def find_shortest_route(self):
        route = Route(self, (self.starting_location,), ())
        queue = [route]
        completed_routes = []
        stuck_routes = []
        n = 0

        while queue:
            n += 1
            route = queue.pop(0)

            breakpoint() if n % 1000 == 0 else None

            for location in route.next_locations:
                route.visit_next_location(location)

                if route.completed:
                    completed_routes.append(route)
                elif route.stuck:
                    stuck_routes.append(route)
                else:
                    queue.append(route)

        sorted_routes = sorted(completed_routes, key=lambda r: r.distance)
        shortest_route = sorted_routes[0]
        return shortest_route


class Route:
    def __init__(self, router, visited, distances):
        self.router = router
        self.visited = visited
        self.distances = distances

    @property
    def distance(self):
        return sum(self.distances)

    @cached_property
    def location(self):
        return self.visited[-1]

    @property
    def next_locations(self):
        locations = []
        for location in self.router.legs[self.location]:
            if location not in self.visited:
                locations.append(location)
        return locations

    def visit_next_location(self, location):
        distance = self.router.leg_distances[self.location]
        self.visited += (location,)
        self.distances += (distance,)
        return self

    def clone(self):
        return Route(self.router, self.visited, self.distances)


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-09.txt')

    TEST_INPUT = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

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
        router = SantaRouter(input)
        print(router.location_destinations)
        print(router.starting_location)
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()


#
# Main
#
problem = DailyPuzzle()
problem.solve()
