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
        import pprint
        pprint.pprint([path.combos for path in self.accepted_paths])
        return sum(path.combos for path in self.accepted_paths)

    @cached_property
    def accepted_paths(self):
        # A WorkflowPath is made up of RuleSteps
        # To branch, take last step and find next workflow
        accepted_paths = []
        first_workflow = self.workflows['in']
        path_heap = [Path([first_workflow.first_step])]

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

    def rating_is_accepted(self, rating):
        stops = list('AR')
        result = 'in'

        while result not in stops:
            workflow = self.workflows[result]
            result = workflow.process_rating(rating)

        return result == 'A'


class Path:
    def __init__(self, steps):
        self.steps = list(steps)

    @cached_property
    def combos(self):
        x = self.category_count('x')
        m = self.category_count('m')
        a = self.category_count('a')
        s = self.category_count('s')
        counts = [x, m, a, s]
        combos = math.prod(counts)
        print(combos, counts)
        return combos

        for step in self.steps:
            print(step)
            counts.append(step.count)

        breakpoint()
        return math.prod(counts)

    def category_count(self, category):
        low = 1
        high = 4000

        for step in self.steps:
            if step.category != category:
                continue
            if step.low > low:
                low = step.low
            if step.high < high:
                high = step.high
            print(category, low, high, step)

        if low > high:
            return 0

        return high - low + 1

    @cached_property
    def end_step(self):
        return self.steps[-1]

    @cached_property
    def destination(self):
        return self.end_step.destination

    @cached_property
    def accepted(self):
        return self.destination == 'A'

    @cached_property
    def completed(self):
        return self.destination in ('A', 'R')

    @property
    def in_progress(self):
        return not self.completed

    @cached_property
    def branches(self):
        new_paths = []

        for step in self.next_steps:
            new_path = self.add_step(step)
            new_paths.append(new_path)

        return new_paths

    @cached_property
    def next_steps(self):
        if self.completed:
            return []
        elif type(self.destination) == WorkflowRule:
            rule = self.destination
            return rule.next_steps
        else:
            workflow = self.destination
            return [workflow.first_step]

    def add_step(self, step):
        steps = self.steps + [step]
        return Path(steps)

    def __repr__(self):
        return f"<Path result={self.destination} steps={self.steps}>"


class Step:
    def __init__(self, origin, destination, category=None, lo_hi=None):
        self.origin = origin
        self.destination = destination
        self.category = category
        self.lo_hi = lo_hi

    @cached_property
    def low(self):
        if not self.lo_hi:
            return None
        return self.lo_hi[0]

    @cached_property
    def high(self):
        if not self.lo_hi:
            return None
        return self.lo_hi[1]

    def __repr__(self):
        start = getattr(self.origin, 'id', self.origin)
        end = getattr(self.destination, 'id', self.destination)
        route = f"{start}->{end}"
        return f"<Step {route} category={self.category} range={self.lo_hi}>"


class ExtractWorkflow:
    def __init__(self, extract, input):
        self.extract = extract
        self.input = input.strip()

    @cached_property
    def name(self):
        raw, _ = self.input.split('{')
        return raw.strip()

    @cached_property
    def id(self):
        return f"w:{self.name}"

    @cached_property
    def rules(self):
        rules = []
        _, raw = self.input.split('{')
        rules_input = raw[:-1]
        for rule_input in rules_input.split(','):
            rule = WorkflowRule(self, rule_input)
            rules.append(rule)
        return rules

    @cached_property
    def first_step(self):
        return Step(self, self.rules[0])

    def rule_after(self, rule):
        index = self.rules.index(rule)
        return self.rules[index+1]

    def process_rating(self, rating):
        for rule in self.rules:
            if rule.applies_to_rating(rating):
                    return rule.result
        raise Exception(f"No rules in workflow {self} applied to rating {rating}")

    def __repr__(self):
        return f"<Workflow {self.name}>"


class WorkflowRule:
    def __init__(self, workflow, input):
        self.workflow = workflow
        self.input = input.strip()

    @cached_property
    def id(self):
        index = self.workflow.rules.index(self)
        return f"r{index}:{self.workflow.name}"

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
    def workflows(self):
        return self.workflow.extract.workflows

    @cached_property
    def true_cases(self):
        if not self.condition:
            return 1
        elif self.operator == '<':
            return self.value - 1
        else:
            return MAX_VALUE - self.value

    @cached_property
    def false_cases(self):
        return MAX_VALUE - self.true_cases

    @cached_property
    def true_low_high(self):
        if not self.condition:
            return None

        if self.operator == '<':
            low = 1
            high = self.value - 1
        else:
            low = MAX_VALUE - self.value
            high = MAX_VALUE

        return (low, high)

    @cached_property
    def false_low_high(self):
        if not self.condition:
            return None

        true_low, true_high = self.true_low_high

        if true_low == 1:
            low = true_high + 1
            high = MAX_VALUE
        else:
            low = 1
            high = true_low - 1

        return (low, high)

    @cached_property
    def true_step(self):
        destination = self.workflows.get(self.result)
        result = destination if destination else self.result
        return Step(self, result, self.category, self.true_low_high)

    @cached_property
    def false_step(self):
        if not self.condition:
            return None

        next_rule = self.workflow.rule_after(self)
        return Step(self, next_rule, self.category, self.false_low_high)

    @cached_property
    def next_steps(self):
        steps = [self.true_step]
        if self.false_step:
            steps.append(self.false_step)
        return steps

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

    def __repr__(self):
        return f"<Rule workflow={self.workflow.name} {self.input}>"


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
