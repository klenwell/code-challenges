"""
Advent of Code 2015 - Day 09
https://adventofcode.com/2015/day/9

Day 9: All in a Single Night
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class SantaRouter:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def shortest_route(self):
        all_routes = self.travel_all_routes()
        sorted_routes = sorted(all_routes, key=lambda r: r.distance)
        return sorted_routes[0]

    @cached_property
    def longest_routes(self):
        all_routes = self.travel_all_routes()
        sorted_routes = sorted(all_routes, key=lambda r: r.distance)
        return sorted_routes[-1]

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
    def locations(self):
        return list(self.legs.keys())

    @cached_property
    def legs(self):
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
    def leg_distances(self):
        mapped = {}
        for l1, l2, distance in self.location_pairs:
            mapped[(l1, l2)] = distance
            mapped[(l2, l1)] = distance
        return mapped

    @property
    def starting_location(self):
        sorted_locations = sorted(self.legs.items(), key=lambda kv: len(kv[1]))
        return sorted_locations[0][0]

    def travel_all_routes(self):
        queue = []
        completed_routes = []
        stuck_routes = []
        n = 0

        # Create a route for each location
        for location in self.locations:
            route = Route(self, (location,), ())
            queue.append(route)

        while queue:
            n += 1
            route = queue.pop(0)

            info(f"queue={len(queue)} completed={len(completed_routes)}", 10000)

            for location in route.next_locations:
                clone = route.clone()
                clone.visit_next_location(location)

                if clone.completed:
                    completed_routes.append(clone)
                elif clone.stuck:
                    stuck_routes.append(clone)
                else:
                    queue.append(clone)

        return completed_routes


class Route:
    def __init__(self, router, visited, distances):
        self.router = router
        self.visited = visited
        self.distances = distances

    @property
    def distance(self):
        return sum(self.distances)

    @property
    def location(self):
        return self.visited[-1]

    @property
    def completed(self):
        return not set(self.router.locations).symmetric_difference(self.visited)

    @property
    def stuck(self):
        return not self.completed and not self.next_locations

    @property
    def next_locations(self):
        locations = []
        for location in self.router.legs[self.location]:
            if location not in self.visited:
                locations.append(location)
        return locations

    def visit_next_location(self, next_location):
        key = (self.location, next_location)
        distance = self.router.leg_distances[key]
        self.visited += (next_location,)
        self.distances += (distance,)
        return self

    def clone(self):
        return Route(self.router, self.visited, self.distances)

    def __repr__(self):
        start = self.visited[0]
        return f"<Route start={start} location={self.location} distance={self.distance}>"


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
        router = SantaRouter(input)
        assert router.shortest_route.distance < 510, router.shortest_route
        return router.shortest_route.distance

    @property
    def second(self):
        input = self.file_input
        router = SantaRouter(input)
        return router.longest_routes.distance

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        router = SantaRouter(input)
        shortest_route = router.shortest_route
        assert shortest_route.distance == 605, shortest_route
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        router = SantaRouter(input)
        longest_routes = router.longest_routes
        assert longest_routes.distance == 982, longest_routes
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
