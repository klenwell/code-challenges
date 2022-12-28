"""
Advent of Code 2022 - Day 19
https://adventofcode.com/2022/day/19
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import re
from enum import Enum


INPUT_FILE = path_join(INPUT_DIR, 'day-19.txt')

TEST_INPUT = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

RESOURCES = ['ore', 'clay', 'obsidian', 'geode']


class Factory:

    @staticmethod
    def from_blueprint(blueprint):
        # ID
        id, tail = blueprint.split(':')
        bluprint_id = [int(d) for d in re.findall(r'-?\d+', id)][0]

        # Costs
        costs = {}
        cost_sheets = tail.split('.')[:-1]
        for n, sheet in enumerate(cost_sheets):
            robot = RESOURCES[n]
            prices = [int(d) for d in re.findall(r'-?\d+', sheet)]
            extra_cost = prices[1] if robot in ('obsidian', 'geode') else None
            costs[robot] = (prices[0], extra_cost)

        # Robots
        robots = {}
        for robot in RESOURCES:
            robots[robot] = 0
        robots['ore'] = 1

        return Factory(bluprint_id, costs, robots)

    def __init__(self, blueprint_id, costs, robots, resources=None, orders=None):
        self.blueprint_id = int(blueprint_id)
        self.costs = costs.copy()
        self.robots = robots.copy()
        self.resources = resources.copy() if resources else self.init_resources()
        self.orders = orders.copy() if orders else []

    @property
    def possible_orders(self):
        """Figure out all possible orders (including none) for a factory in a turn
        given current resources.
        """
        orders = [None]
        for robot in self.robots.keys():
            if self.can_afford(robot):
                orders.append(robot)
        return orders

    @property
    def minute(self):
        return len(self.orders)

    @property
    def geodes(self):
        return self.resources['geode']

    @property
    def geode_bots(self):
        return self.robots['geode']

    @property
    def quality(self):
        return self.geodes * self.blueprint_id

    @property
    def hash(self):
        inputs = [self.minute]
        for type in RESOURCES:
            inputs += [self.robots[type], self.resources[type]]
        return ':'.join([str(i) for i in inputs])

    @property
    def sort_key(self):
        return (self.robots['geode'], self.robots['obsidian'])

    def init_resources(self):
        resources = {}
        for resource in RESOURCES:
            resources[resource] = 0
        return resources

    def maximize_geodes(self, minutes):
        completed = []
        purged = 0
        lf = 1000  # log frequency
        queue = [self.clone()]
        n = 0
        hashes = []

        while queue:
            n += 1

            factory = queue.pop(0)
            print(n, len(queue), len(completed), purged, factory) if n % lf == 0 else None

            # Purge
            if n % 1000 == 0:
                before = len(queue)
                queue = factory.purge_redundancies(queue)
                purged += before - len(queue)
                print('redundancies', before - len(queue), factory.hash) if n % lf == 0 else None

            if n % 100 == 0:
                before = len(queue)
                queue = factory.purge_suboptimals(queue)
                purged += before - len(queue)
                print('suboptimals', before - len(queue), factory.resources) if n % lf == 0 else None

            # Decimate
            # if max_obsids > 1 and n % lf == 0 and len(queue) > 10000:
            #     before = len(queue)
            #     queue = factory.decimate(queue)
            #     purged += before - len(queue)
            #     print('purged', before - len(queue), factory, factory.sort_key)

            # Purge laggards
            # if n % 1000 == 0:
            #     if max_geodes > 0:
            #         before = len(queue)
            #         queue = factory.decimate(queue)
            #         purged += before - len(queue)
            #         print('purged', purged, factory, factory.sort_key)


            for order in factory.possible_orders:
                clone = factory.clone()
                clone.order(order)

                if clone.minute >= minutes:
                    completed.append(clone)
                else:
                    queue.append(clone)

        clones = sorted(completed, key=lambda f: f.geodes)
        optimal = clones[-1]
        print(len(completed), optimal, clones[0])
        #breakpoint()
        return optimal

    def purge_redundancies(self, clones):
        uniques = []
        redundancies = {}
        for clone in clones:
            if clone.hash in redundancies:
                redundancies[clone.hash] += 1
            else:
                redundancies[clone.hash] = 1
                uniques.append(clone)
        return uniques

    def meets_specs(self, min_geode_bots, minute):
        max_ore_cost = max(c[0] for c in self.costs.values())
        min_ore_cost = min(c[0] for c in self.costs.values())
        max_clay_cost = self.costs['obsidian'][1]
        max_obsid_cost = self.costs['geode'][1]

        ore_bots_ok = self.robots['ore'] <= max_ore_cost
        clay_bots_ok = self.robots['clay'] <= max_clay_cost
        obsid_bots_ok = self.robots['obsidian'] <= max_obsid_cost
        geo_bots_ok = self.robots['geode'] >= min_geode_bots if self.minute == minute else True

        ore_ok = self.resources['ore'] <= max_ore_cost + 1 if ore_bots_ok else True
        #clay_ok = self.resources['clay'] <= max_clay_cost if clay_bots_ok else True
        #obsid_ok = self.resources['obsidian'] <= max_obsid_cost if obsid_bots_ok else True
        obsid_ok = self.resources['obsidian'] <= max_obsid_cost + min_ore_cost

        specs = [
            ore_bots_ok,
            #clay_bots_ok,
            #obsid_bots_ok,
            geo_bots_ok,
            ore_ok,
            #clay_ok,
            obsid_ok
        ]

        return all(specs)

    def purge_suboptimals(self, clones):
        optimals = []
        min_geode_bots, minute = max((c.geode_bots, c.minute) for c in clones)
        for clone in clones:
            if clone.meets_specs(min_geode_bots, minute):
                optimals.append(clone)
        return optimals

    def decimate(self, clones, ratio=.5):
        idx = int(len(clones) * (1 - ratio))
        sorted_clones = sorted(clones, key=lambda f: f.sort_key, reverse=True)
        return sorted_clones[:idx]

    def clone(self):
        return Factory(self.blueprint_id, self.costs, self.robots, self.resources, self.orders)

    def can_afford(self, robot):
        ore_cost, extra_cost = self.costs[robot]

        if ore_cost > self.resources['ore']:
            return False

        if robot == 'obsidian' and extra_cost > self.resources['clay']:
            return False
        elif robot == 'geode' and extra_cost > self.resources['obsidian']:
            return False

        return True

    def order(self, order):
        self.orders.append(order)
        robot = self.order_robot(order)
        self.harvest()
        self.collect_robot(robot)

    def order_robot(self, order):
        if order is None:
            return None

        ore_cost, extra_cost = self.costs[order]

        self.resources['ore'] -= ore_cost

        if order == 'obsidian':
            self.resources['clay'] -= extra_cost
        elif order == 'geode':
            self.resources['obsidian'] -= extra_cost

        return order

    def harvest(self):
        for resource, count in self.robots.items():
            self.resources[resource] += count
        return self.resources

    def collect_robot(self, robot):
        if robot:
            self.robots[robot] += 1
        return self.robots

    def __repr__(self):
        f = '<Factory id={} costs={} geodes={} quality={} hash={}>'
        return f.format(self.blueprint_id, self.costs, self.geodes, self.quality, self.hash)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        blueprints = TEST_INPUT.split('\n')
        minutes = 24

        # Factory 1 Test
        factories = [Factory.from_blueprint(bp) for bp in blueprints]
        first = factories[0].maximize_geodes(minutes)
        assert first.quality == 9, first

        # Factory 2 Test
        second = factories[1].maximize_geodes(minutes)
        assert second.quality == 24, second

        solution = first.quality + second.quality
        assert solution == 33
        return solution


    @property
    def first(self):
        blueprints = self.input_lines
        minutes = 24
        logs = []

        import time, pprint

        sum = 0
        for bp in blueprints:
            t0 = time.process_time()
            factory = Factory.from_blueprint(bp)
            factory = factory.maximize_geodes(minutes)
            logs.append((factory, time.process_time() - t0))
            sum += factory.quality

        pprint.pprint(logs)
        return sum
        # 1234 too low

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
