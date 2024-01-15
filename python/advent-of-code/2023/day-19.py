"""
Advent of Code 2023 - Day 19
https://adventofcode.com/2023/day/19
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR
import json


class Extract:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def workflows(self):
        workflows = {}
        input, _ = self.input.split('\n\n')
        for line in input.split('\n'):
            workflow = Workflow(line)
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
            if self.is_accepted(rating):
                sum += rating.sum
        return sum

    def is_accepted(self, rating):
        stops = list('AR')
        result = 'in'

        while result not in stops:
            workflow = self.workflows[result]
            result = workflow.process_rating(rating)

        return result == 'A'


class Workflow:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def name(self):
        raw, _ = self.input.split('{')
        return raw.strip()

    @cached_property
    def rules(self):
        rules = []
        _, raw = self.input.split('{')
        rules_input = raw[:-1]
        for rule_input in rules_input.split(','):
            rule = WorkflowRule(rule_input)
            rules.append(rule)
        return rules

    def process_rating(self, rating):
        for rule in self.rules:
            if rule.applies_to_rating(rating):
                    return rule.result
        raise Exception(f"No rules in workflow {self} applied to rating {rating}")


class WorkflowRule:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def condition(self):
        if ':' not in self.input:
            return None
        raw, _ = self.input.split(':')
        return raw

    @cached_property
    def result(self):
        if ':' not in self.input:
            return self.input
        _, raw = self.input.split(':')
        return raw

    @cached_property
    def operator(self):
        return self.condition[1]

    @cached_property
    def category(self):
        if not self.condition:
            return None
        return self.condition[0]

    @cached_property
    def value(self):
        if not self.condition:
            return None
        return int(self.condition[2:])

    def applies_to_rating(self, rating):
        if not self.condition:
            return True

        rating_value = rating.categories[self.category]
        if self.operator == '>':
            return rating_value > self.value
        elif self.operator == '<':
            return rating_value < self.value
        else:
            return Exception(f"Unexpected rule comparator: {self.operator}")


class PartRating:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def categories(self):
        key_values = {}
        assignments = self.input[1:-1]
        for assignment in assignments.split(','):
            cat, val = assignment.split('=')
            key_values[cat] = int(val)
        return key_values

    @cached_property
    def sum(self):
        return sum(self.categories.values())

    def __repr__(self):
        return f"<PartRating sum={self.sum} {self.ratings}>"


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
        extract = Extract(input)

        assert extract.sum == 19114
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
