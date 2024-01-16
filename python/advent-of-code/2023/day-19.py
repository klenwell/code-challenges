"""
Advent of Code 2023 - Day 19
https://adventofcode.com/2023/day/19
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info
import math


MAX_VALUE = 4000


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
        return sum([path.combos for path in self.accepted_paths])

    @cached_property
    def accepted_paths(self):
        # A WorkflowPath is made up of RuleSteps
        # To branch, take last step and find next workflow
        accepted_paths = []
        first_workflow = self.workflows['in']
        path_heap = [Path(first_workflow)]

        while path_heap:
            info(len(path_heap), 100)
            path = path_heap.pop()
            for new_path in path.branches:
                if new_path.accepted:
                    print('ACCEPT', new_path)
                    accepted_paths.append(new_path)
                elif path.in_progress:
                    path_heap.append(new_path)

        breakpoint()
        return accepted_paths

    def rating_is_accepted(self, rating):
        stops = list('AR')
        result = 'in'

        while result not in stops:
            workflow = self.workflows[result]
            result = workflow.process_rating(rating)

        return result == 'A'


class Path:
    def __init__(self, workflow, steps=None):
        self.workflow = workflow
        if not steps:
            self.steps = []
        else:
            self.steps = list(steps)

    @cached_property
    def combos(self):
        return math.prod([step.combos for step in self.steps])

    @cached_property
    def workflows(self):
        return self.workflow.extract.workflows

    @cached_property
    def branches(self):
        new_paths = []
        continuing_step = None

        for rule in self.workflow.rules:
            true_step, false_step = rule.to_steps(continuing_step)
            continuing_step = false_step
            new_path = self.add_step(true_step)
            new_paths.append(new_path)

        return new_paths

    @property
    def last_step(self):
        if not self.steps:
            return None
        return self.steps[-1]

    @property
    def result(self):
        if not self.last_step:
            return None
        return self.last_step.result

    @property
    def accepted(self):
        if not self.last_step:
            return False
        return self.result == 'A'

    @property
    def in_progress(self):
        return self.result not in ('A', 'R')

    def add_step(self, step):
        self.steps.append(step)
        next_workflow = self.workflows.get(step.destination)
        return Path(next_workflow, self.steps)

    def __repr__(self):
        return f"<Path result={self.result} steps={self.steps}>"


class ExtractWorkflow:
    def __init__(self, extract, input):
        self.extract = extract
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
            rule = WorkflowRule(self, rule_input)
            rules.append(rule)
        return rules

    def process_rating(self, rating):
        for rule in self.rules:
            if rule.applies_to_rating(rating):
                    return rule.result
        raise Exception(f"No rules in workflow {self} applied to rating {rating}")


class WorkflowRule:
    def __init__(self, workflow, input):
        self.workflow = workflow
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

    @cached_property
    def true_cases(self):
        if self.operator == '<':
            return self.value - 1
        else:
            return MAX_VALUE - self.value

    @cached_property
    def false_cases(self):
        return MAX_VALUE - self.true_cases

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

    def to_steps(self, incomplete_step):
        combos = 1
        if incomplete_step:
            combos = incomplete_step.combos
        if not self.condition:
            true_step = RuleStep(self, self.result, combos)
            false_step = None
        else:
            true_step = RuleStep(self, self.result, combos * self.true_cases)
            false_step = RuleStep(self, None, combos * self.false_cases)
        return true_step, false_step


class RuleStep:
    def __init__(self, rule, destination, combos):
        self.rule = rule
        self.origin = self.rule.workflow.name
        self.destination = destination
        self.combos = combos

    @cached_property
    def result(self):
        return self.destination

    def __repr__(self):
        route = f"{self.origin}->{self.destination}"
        return f"<RuleStep {route} combos={self.combos}>"


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
        input = self.TEST_INPUT
        extract = Extract(input)
        assert extract.distinct_combinations == 167409079868000, extract.distinct_combinations
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
