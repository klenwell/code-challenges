"""
Advent of Code 2023 - Day 19
https://adventofcode.com/2023/day/19
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info

from models.day_19.path import Path
from models.day_19.step import RatingStep
from models.day_19.workflow import ExtractWorkflow
from models.day_19.ratings import PartRating, PossibleRatings


class Extract:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def workflows(self):
        workflows = {}
        input, _ = self.input.split('\n\n')
        for line in input.split('\n'):
            workflow = ExtractWorkflow(self, line)
            workflows[workflow.name] = workflow
        return workflows

    @cached_property
    def ratings(self):
        ratings = []
        _, input = self.input.split('\n\n')
        for line in input.split('\n'):
            rating = PartRating(line)
            ratings.append(rating)
        return ratings

    @cached_property
    def sum(self):
        sum = 0
        for rating in self.ratings:
            if self.rating_is_accepted(rating):
                sum += rating.sum
        return sum

    @cached_property
    def distinct_combinations(self):
        accepted = self.accepted_paths
        breakpoint()
        import pprint
        pprint.pprint([path.combos for path in self.accepted_paths])
        return sum(path.combos for path in self.accepted_paths)

    @cached_property
    def accepted_paths(self):
        accepted_paths = []
        path_heap = [Path([self.first_step])]

        while path_heap:
            info(len(path_heap), 100)
            path = path_heap.pop()
            #print(path)
            for new_path in path.branches:
                if new_path.accepted:
                    print('ACCEPT', new_path.combos, new_path)
                    accepted_paths.append(new_path)
                elif path.in_progress:
                    path_heap.append(new_path)

        return accepted_paths

    @property
    def first_step(self):
        first_workflow = self.workflows['in']
        ratings = PossibleRatings.max_ranges()
        return RatingStep(first_workflow, first_workflow.rules[0], ratings)

    def rating_is_accepted(self, rating):
        stops = list('AR')
        result = 'in'

        while result not in stops:
            workflow = self.workflows[result]
            result = workflow.process_rating(rating)

        return result == 'A'


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-19.txt')

    TEST_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        extract = Extract(input)
        return extract.sum

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        extract = Extract(input)
        assert extract.sum == 19114
        return 'passed'

    @property
    def test2(self):
        expected = 167409079868000
        input = self.TEST_INPUT
        extract = Extract(input)
        result = extract.distinct_combinations

        def errs(val, expected):
            diff = expected - val
            verb = 'over' if diff < 0 else 'under'
            pct = 100.0 * diff / expected
            return f"got {val} expected {expected} {verb} by {abs(diff)} ({abs(pct)}%)"

        assert result == expected, errs(result, expected)
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
