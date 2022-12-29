"""
Advent of Code 2022 - Day 19
https://adventofcode.com/2022/day/19
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import re
from enum import Enum
import time, pprint


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
    def recommended_orders(self):
        """Try to filter out orders that would be a waste of time.
        """
        orders = []
        for robot in self.possible_orders:
            if robot in self.max_costs and self.robots[robot] >= self.max_costs[robot]:
                continue
            orders.append(robot)
        return orders

    @cached_property
    def max_costs(self):
        return {
            'ore': max(c[0] for c in self.costs.values()),
            'clay': self.costs['obsidian'][1],
            'obsidian': self.costs['geode'][1]
        }

    @property
    def minute(self):
        return len(self.orders)

    @property
    def geodes(self):
        return self.resources['geode']

    @property
    def quality(self):
        return self.geodes * self.blueprint_id

    @property
    def hash(self):
        inputs = [self.minute]
        for type in RESOURCES:
            inputs += [self.robots[type], self.resources[type]]
        return ':'.join([str(i) for i in inputs])

    def init_resources(self):
        resources = {}
        for resource in RESOURCES:
            resources[resource] = 0
        return resources

    def maximize_geodes(self, minutes):
        completed = []
        purged = 0
        queue = [self.clone()]
        n = 0
        minute = 1

        while queue:
            n += 1

            factory = queue.pop(0)
            if factory.minute > minute:
                minute = factory.minute

                before = len(queue)
                queue = factory.purge_redundancies(queue)

                if minute > 16:
                    queue = factory.purge_suboptimals(queue)

                # Cap
                min_cap = .75
                max_cap = .6
                cap_start_minute = 10
                steps = minutes - cap_start_minute
                cap_step = (min_cap - max_cap) / steps
                cap_minute = minute - cap_start_minute
                queue_ratio = min_cap - (cap_minute * cap_step)
                dynamic_cap = int(len(queue) * queue_ratio)
                hard_cap = 50000
                cap = min(dynamic_cap, hard_cap)
                if len(queue) > cap and minute > cap_start_minute:
                    sorted_clones = sorted(queue, key=lambda c: c.value, reverse=True)
                    print('capped', (queue_ratio, cap), (sorted_clones[0].value, sorted_clones[cap].value, sorted_clones[-1].value), len(sorted_clones) - cap)
                    queue = sorted_clones[:cap]

                purged += before - len(queue)
                print(minute, n, len(queue), purged, factory)

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

        print('purge_redundancies', len(clones) - len(uniques))
        return uniques

    def purge_suboptimals(self, clones):
        optimals = []

        if not clones:
            return clones

        max_bots = {}
        for resource in RESOURCES:
            max_bots[resource] = max(c.robots[resource] for c in clones)

        for clone in clones:
            if clone.meets_specs(max_bots):
                optimals.append(clone)

        print('purge_suboptimals', len(clones) - len(optimals))
        return optimals

    def meets_specs(self, max_bots):
        ore_bots_ok = self.robots['ore'] <= self.max_costs['ore']

        #ore_ok = self.resources['ore'] <= self.max_costs['ore'] + 1
        #clay_ok = self.resources['clay'] <= max_clay_cost if clay_bots_ok else True
        #obsid_ok = self.resources['obsidian'] <= max_obsid_cost if obsid_bots_ok else True

        bot_productivity_ok = True
        for resource in RESOURCES:
            if self.robots[resource] == 0 and max_bots[resource] > 1:
                bot_productivity_ok = False
                break

        bot_allocation_ok = True
        for resource in self.max_costs.keys():
            if self.robots[resource] > self.max_costs[resource]:
                bot_allocation_ok = False
                break

        output_ok = True

        specs = [
            ore_bots_ok,
            #ore_ok,
            #clay_ok,
            #obsid_ok,
            #bot_productivity_ok,
            bot_allocation_ok
        ]

        return all(specs)

    @cached_property
    def robot_values(self):
        values = {}
        values['ore'] = self.costs['ore'][0]
        values['clay'] = self.costs['clay'][0]
        values['obsidian'] = self.costs['obsidian'][0] + (self.costs['obsidian'][1] * values['clay'])
        values['geode'] = self.costs['geode'][0] + (self.costs['geode'][1] * values['obsidian'])
        return values

    @property
    def value(self):
        value = 0
        for robot, count in self.robots.items():
            value += self.robot_values[robot] * count
        return value

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
        #breakpoint()
        blueprints = self.input_lines
        minutes = 24
        logs = []

        sum = 0
        for bp in blueprints:
            t0 = time.process_time()
            factory = Factory.from_blueprint(bp)
            factory = factory.maximize_geodes(minutes)
            logs.append((factory, time.process_time() - t0))
            sum += factory.quality

        pprint.pprint(logs)
        assert sum == 1480, sum
        return sum
        # 1234 too low
        # 1237 too low

    @property
    def test2(self):
        blueprints = TEST_INPUT.split('\n')
        minutes = 32

        # Factory 1 Test
        factories = [Factory.from_blueprint(bp) for bp in blueprints]
        first = factories[0].maximize_geodes(minutes)
        assert first.geodes == 56, first

        # Factory 2 Test
        second = factories[1].maximize_geodes(minutes)
        assert second.geodes == 62, second

        solution = first.geodes * second.geodes
        return solution

    @property
    def second(self):
        blueprints = self.input_lines[:3]
        minutes = 32

        logs = []

        product = 1
        for bp in blueprints:
            t0 = time.process_time()
            factory = Factory.from_blueprint(bp)
            factory = factory.maximize_geodes(minutes)
            logs.append((factory, time.process_time() - t0))
            product *= factory.geodes

        pprint.pprint(logs)
        return product

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
