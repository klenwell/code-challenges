"""
Advent of Code 2022 - Day 16
https://adventofcode.com/2022/day/16
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import re


INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')

TEST_INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def extract_numbers(str):
    return [int(d) for d in re.findall(r'-?\d+', str)]


class Valve:
    def __init__(self, scan):
        flow_rate, tunnels = scan.split(';')
        self.label = self.extract_label(flow_rate)
        self.flow = extract_numbers(flow_rate)[0]
        self.neighbors = self.extract_neighbors(tunnels)

    def extract_label(self, input):
        label, _ = input.split(' has flow')
        _, label = label.split(' ')
        return label

    def extract_neighbors(self, input):
        _, valves = input.split('valve')
        valves = valves[2:] if valves.startswith('s') else valves[1:]
        return [label.strip() for label in valves.split(',')]

    def __repr__(self):
        return f"<Valve lable={self.label} flow={self.flow} neighbors={self.neighbors}>"


class PipeNetwork:
    def __init__(self, valve_scans):
        self.valves = [Valve(scan) for scan in valve_scans]

        # Memoize shortcuts
        self.shortest_paths = {}

    @cached_property
    def valves_by_label(self):
        index = {}
        for valve in self.valves:
            index[valve.label] = valve
        return index

    @cached_property
    def graph(self):
        graph = {}
        for label, valve in self.valves_by_label.items():
            graph[label] = valve.neighbors
        return graph

    @cached_property
    def working_valves(self):
        return set([valve for valve in self.valves if valve.flow > 0])

    def find_shortest_path(self, start_label, end_label):
        key = (start_label, end_label)

        if key in self.shortest_paths:
            return self.shortest_paths[key]

        initial_path = [start_label]
        queue = [initial_path]
        completed = []

        while queue:
            path = queue.pop(0)
            current_valve_label = path[-1]
            # print(key, current_valve_label, path, len(queue))

            for next_valve_label in self.graph[current_valve_label]:
                if next_valve_label in path:
                    continue

                new_path = path + [next_valve_label]

                if next_valve_label == end_label:
                    completed.append(new_path)
                else:
                    queue.append(new_path)

        shortest_path = sorted(completed, key=lambda p: len(p))[0]
        # print('shortest', len(completed), shortest_path)

        self.shortest_paths[key] = shortest_path
        return shortest_path


class ElfPlumber:
    #
    # Public
    #
    def __init__(self, network, steps=None):
        self.network = network
        self.steps = steps.copy() if steps else ['AA']

    def maximize_release(self, minutes):
        queue = [self]
        completed = []
        pruned = 0
        minute = 0

        while queue:
            plumber = queue.pop(0)

            # Branch
            unopened_valves = plumber.unopened_working_valves

            if not unopened_valves:
                plumber.stop_at_minute(minutes)
                completed.append(plumber)

            for valve in unopened_valves:
                clone = plumber.clone()
                clone.visit(valve)

                if clone.minute >= minutes:
                    clone.stop_at_minute(minutes)
                    completed.append(clone)
                else:
                    queue.append(clone)

            if not queue:
                break

            # Prune
            queue = sorted(queue, key=lambda n: n.minute)
            plumber = queue[0]
            if plumber.minute > minute:
                minute = plumber.minute
                before = len(queue)

                queue = plumber.prune(queue)

                pruned += before - len(queue)
                print(minute, len(queue), pruned, len(completed), plumber)

        plumbers = sorted(completed, key=lambda n: n.release)
        return plumbers[-1]

    #
    # Properties
    #
    @property
    def logs(self):
        logs = []
        open_valves = ()

        for min in range(self.minute+1):
            logs.append(open_valves)
            valve_added = self.steps[min-1] if self.steps[min] == 'OPEN' else None

            if valve_added:
                open_valves += (valve_added,)

        logs.append(open_valves)
        return logs

    @property
    def open_valves(self):
        return self.logs[-1]

    @property
    def unopened_working_valves(self):
        return self.working_valves - set(self.open_valves)

    @property
    def working_valves(self):
        return set([v.label for v in self.network.working_valves])

    @property
    def current_valve(self):
        i = 0
        last_step = 'OPEN'

        while last_step == 'OPEN':
            i -= 1
            last_step = self.steps[i]

        return last_step

    @property
    def minute(self):
        return len(self.steps)-1

    @property
    def release_at_current_minute(self):
        return sum(self.flow_at_minute(m) for m in range(self.minute+1))

    @property
    def release(self):
        return self.release_at_current_minute

    @property
    def redundancy_key(self):
        return (
            self.minute,
            self.current_valve,
            self.release
        )

    @property
    def cohort_key(self):
        return (
            self.minute,
            self.current_valve
        )

    @property
    def details(self):
        logs = []
        for minute, step in enumerate(self.steps):
            step = step if step != 'OPEN' else self.steps[minute-1]
            open_valves = sorted(self.logs[minute])
            pressure = self.flow_at_minute(minute)
            f = "Minute {} at {}: Valves {} released {} pressure."
            log = f.format(minute, step, open_valves, pressure)
            logs.append(log)
        return logs

    #
    # Methods
    #
    def clone(self):
        return ElfPlumber(self.network, self.steps)

    def stop_at_minute(self, minute):
        while self.minute < minute:
            self.wait()

        self.steps = self.steps[:minute+1]
        return self

    def visit(self, label):
        path = self.find_shortest_path_to(label)

        # Walk path updating steps and logs as we go.
        # Path will start with current valve already in steps so skip it.
        for step in path[1:]:
            self.steps.append(step)

        # Now open the valve and log progress
        self.steps.append('OPEN')

        return self

    def wait(self):
        self.steps.append(self.current_valve)
        return self

    def prune(self, clones):
        # clones = self.prune_redundancies(clones)
        clones = self.prune_cohorts(clones)
        return clones

    def prune_redundancies(self, clones):
        # This does not help. :)
        uniques = []
        redundancies = {}

        for clone in clones:
            if clone.redundancy_key in redundancies:
                redundancies[clone.redundancy_key] += 1
            else:
                redundancies[clone.redundancy_key] = 1
                uniques.append(clone)

        return uniques

    def prune_cohorts(self, clones):
        """Cohorts are made up of clones at same point at same minute. Those with lower
        flow are purged.
        """
        leaders = []
        cohorts = {}

        for clone in clones:
            if clone.cohort_key in cohorts:
                cohorts[clone.cohort_key].append(clone)
            else:
                cohorts[clone.cohort_key] = [clone]

        for clones in cohorts.values():
            plumbers = sorted(clones, key=lambda p: p.release, reverse=True)
            max_release = plumbers[0].release
            for plumber in plumbers:
                if plumber.release >= max_release:
                    leaders.append(plumber)
                else:
                    break

        return leaders

    def find_shortest_path_to(self, label):
        start = self.current_valve
        return self.network.find_shortest_path(start, label)

    def flow_at_minute(self, minute):
        labels = self.logs[minute]
        return sum(self.network.valves_by_label[l].flow for l in labels)

    def __repr__(self):
        return f"<Plumber minute={self.minute} at={self.current_valve} release={self.release}>"


class PlumberTeam(ElfPlumber):
    def __init__(self, network, steps=None, logs=None, open_valves=None, elephant_steps=None):
        self.network = network
        self.steps = steps.copy() if steps else ['AA']
        self.elephant_steps = elephant_steps.copy() if elephant_steps else ['AA']
        self.logs = logs.copy() if logs else [()]
        self.open_valves = open_valves if open_valves else ()

    def clone(self):
        return PlumberTeam(self.network, self.steps, self.logs, self.open_valves,
                           self.elephant_steps)

    def maximize_release(self, minutes):
        queue = [self]
        completed = []
        pruned = 0
        minute = 0

        from timeit import default_timer as timer
        t0 = timer()

        while queue:
            team = queue.pop(0)

            # Branch
            unopened_valves = team.unopened_working_valves

            if not unopened_valves:
                team.stop_at_minute(minutes)
                completed.append(team)
            else:
                clones = team.next_move(unopened_valves)
                for clone in clones:
                    if clone.minute >= minutes:
                        clone.stop_at_minute(minutes)
                        completed.append(clone)
                    else:
                        queue.append(clone)

            if not queue:
                break

            # Prune
            queue = sorted(queue, key=lambda n: n.minute)
            team = queue[0]
            if team.minute > minute:
                minute = team.minute
                before = len(queue)

                queue = team.prune(queue)

                pruned += before - len(queue)
                print(minute, len(queue), pruned, len(completed), team, timer()-t0)
                t0 = timer()

        teams = sorted(completed, key=lambda n: n.release)
        return teams[-1]

    def prune(self, clones):
        # clones = self.prune_overlaps(clones)
        clones = self.prune_cohorts(clones)
        return clones

    def prune_overlaps(self, clones):
        # This does not help.
        uniques = []

        for clone in clones:
            overlaps = self.elf_opened.intersection(self.elephant_opened)

            if not overlaps:
                uniques.append(clone)

        return uniques

    def prune_cohorts(self, clones):
        """Cohorts are made up of clones at same point at same minute. Those with lower
        flow are purged.
        """
        leaders = []
        cohorts = {}

        for clone in clones:
            if clone.cohort_key in cohorts:
                cohorts[clone.cohort_key].append(clone)
            else:
                cohorts[clone.cohort_key] = [clone]

        for clones in cohorts.values():
            plumbers = sorted(clones, key=lambda p: p.release_at_current_minute, reverse=True)
            max_release = plumbers[0].release
            for plumber in plumbers:
                if plumber.release >= max_release:
                    leaders.append(plumber)
                else:
                    break

        return leaders

    @property
    def cohort_key(self):
        m = self.minute
        elf_valve = self.steps[m-1] if self.steps[m] == 'OPEN' else self.steps[m]
        elph_steps = self.elephant_steps[m]
        elephant_valve = self.elephant_steps[m-1] if elph_steps == 'OPEN' else elph_steps
        return (
            self.minute,
            elf_valve,
            elephant_valve
        )

    # TODO: Get rid of these, use parent
    @property
    def release_at_current_minute(self):
        return sum(self.flow_at_minute(m) for m in range(self.minute+1))

    @property
    def release(self):
        return self.release_at_current_minute

    def flow_at_minute(self, minute):
        labels = self.team_logs[minute]
        return sum(self.network.valves_by_label[l].flow for l in labels)

    @property
    def team_logs(self):
        logs = []
        open_valves = ()

        for min in range(self.minute+1):
            logs.append(open_valves)
            elf_added = self.steps[min-1] if self.steps[min] == 'OPEN' else None
            elph_added = self.elephant_steps[min-1] if self.elephant_steps[min] == 'OPEN' else None

            if elf_added:
                open_valves += (elf_added,)

            if elph_added:
                open_valves += (elph_added,)

        logs.append(open_valves)
        return logs

    @property
    def elf_opened(self):
        opened = set()
        for n, step in enumerate(self.steps):
            if step == 'OPEN':
                opened.add(self.steps[n-1])
        return opened

    @property
    def elephant_opened(self):
        opened = set()
        for n, step in enumerate(self.elephant_steps):
            if step == 'OPEN':
                opened.add(self.elephant_steps[n-1])
        return opened

    def stop_at_minute(self, minute):
        let_elephant_catch_up = True if self.elf_minute >= self.elephant_minute else False

        if let_elephant_catch_up:
            while self.elephant_minute < self.elf_minute:
                self.elephant_wait()
        else:
            while self.elf_minute < self.elephant_minute:
                self.elf_wait()

        while self.minute < minute:
            self.wait()

        self.steps = self.steps[:minute+1]
        self.elephant_steps = self.elephant_steps[:minute+1]
        self.logs = self.logs[:minute+1]
        return self

    def wait(self):
        self.logs.append(self.open_valves)
        self.elephant_wait()
        self.elf_wait()
        return self

    def elephant_wait(self):
        self.elephant_steps.append(self.current_elephant_valve)
        return self

    def elf_wait(self):
        self.steps.append(self.current_valve)
        return self

    def next_move(self, unopened_valves):
        clones = []

        # Originally, I had both move if they were ready. This was wasteful. Have
        # one move and other will catch up.
        if self.elf_is_ready_to_move():
            clones += self.elf_moves(unopened_valves)
        else:
            clones += self.elephant_moves(unopened_valves)

        return clones

    def elf_moves(self, unopened_valves):
        clones = []
        for valve_label in unopened_valves:
            clone = self.clone()
            clone.visit(valve_label)
            clones.append(clone)
        return clones

    def elephant_moves(self, unopened_valves):
        clones = []
        for valve_label in unopened_valves:
            clone = self.clone()
            clone.elephant_visit(valve_label)
            clones.append(clone)
        return clones

    def elephant_visit(self, valve_label):
        start = self.current_elephant_valve
        path = self.network.find_shortest_path(start, valve_label)

        # Walk path updating steps and logs as we go.
        # Path will start with current valve already in steps so skip it.
        for step in path[1:]:
            self.elephant_steps.append(step)
            self.logs.append(self.open_valves)

        # Now open the valve and log progress
        self.elephant_steps.append('OPEN')
        self.logs.append(self.open_valves)

        # Release won't get logged until next turn
        self.open_valves = self.open_valves + (valve_label,)
        return self

    def elf_is_ready_to_move(self):
        return self.elf_minute <= self.minute

    def elephant_is_ready_to_move(self):
        return self.elephant_minute <= self.minute

    @property
    def minute(self):
        return min(self.elf_minute, self.elephant_minute)

    @property
    def elf_minute(self):
        return len(self.steps)-1

    @property
    def elephant_minute(self):
        return len(self.elephant_steps)-1

    @property
    def current_elephant_valve(self):
        for step in reversed(self.elephant_steps):
            if step != 'OPEN':
                return step

    @property
    def details(self):
        logs = []
        for min in range(self.minute):
            elph_steps = self.elephant_steps[min]
            elf_step = self.steps[min-1] if self.steps[min] == 'OPEN' else self.steps[min]
            elph_step = self.elephant_steps[min-1] if elph_steps == 'OPEN' else elph_steps
            open_valves = sorted(self.team_logs[min])
            pressure = self.flow_at_minute(min)
            f = "Minute {} at {}: Valves {} released {} pressure."
            log = f.format(min, (elf_step, elph_step), open_valves, pressure)
            logs.append(log)
        return logs


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        valve_scans = self.test_input_lines
        minutes = 30

        # Tests
        self.test_plumber(valve_scans)
        self.test_memoization(valve_scans)

        # Solve
        network = PipeNetwork(valve_scans)
        elf = ElfPlumber(network)
        elf = elf.maximize_release(minutes)
        assert elf.release == 1651, elf
        return elf.release

    @property
    def first(self):
        valve_scans = self.input_lines
        minutes = 30

        network = PipeNetwork(valve_scans)
        elf = ElfPlumber(network)
        elf = elf.maximize_release(minutes)
        assert elf.release == 1828, elf
        return elf.release

    @property
    def test2(self):
        valve_scans = self.test_input_lines
        minutes = 26

        network = PipeNetwork(valve_scans)
        team = PlumberTeam(network)
        team = team.maximize_release(minutes)
        assert team.release == 1707, team
        return team.release

    @property
    def second(self):
        valve_scans = self.input_lines
        minutes = 26

        network = PipeNetwork(valve_scans)
        team = PlumberTeam(network)
        team = team.maximize_release(minutes)
        assert team.release == 2292, team
        return team.release

    #
    # Tests
    #
    def test_plumber(self, valve_scans):
        network = PipeNetwork(valve_scans)
        mario = ElfPlumber(network)

        mario.steps += ['OPEN']
        assert mario.current_valve == 'AA'

        mario.steps += ['ZZ']
        assert mario.current_valve == 'ZZ'
        print('passed test_plumber')

    def test_memoization(self, valve_scans):
        network = PipeNetwork(valve_scans)
        path_key = ('AA', 'ZZ')
        aa_zz_path = ['AA', 'BB', 'ZZ']
        network.shortest_paths[path_key] = aa_zz_path

        mario = ElfPlumber(network)
        luigi = mario.clone()
        short_path = mario.find_shortest_path_to('ZZ')

        assert short_path == aa_zz_path, short_path
        assert luigi.network.shortest_paths[path_key] == aa_zz_path, \
            luigi.network.shortest_paths[path_key]

        # Reset
        new_network = PipeNetwork(valve_scans)
        assert network.shortest_paths[path_key] == aa_zz_path, network.shortest_paths
        assert new_network.shortest_paths.get(path_key) is None, new_network.shortest_paths
        print('passed test_memoization')

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
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
