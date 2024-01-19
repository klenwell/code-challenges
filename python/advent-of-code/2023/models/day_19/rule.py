from functools import cached_property
from models.day_19.step import Step
from models.day_19.ratings import MAX_VALUE


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
        if not self.condition:
            return None
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
    def true_low_high(self):
        if not self.condition:
            return None

        if self.operator == '<':
            low = 1
            high = self.value - 1
        else:
            low = self.value + 1
            high = MAX_VALUE

        return (low, high)

    @cached_property
    def false_low_high(self):
        if not self.condition:
            return None

        true_low, true_high = self.true_low_high

        if self.operator == '<':
            low = self.value
            high = MAX_VALUE
        else:
            low = 1
            high = self.value

        return (low, high)

    @cached_property
    def true_branch(self):
        destination = self.workflows.get(self.result)
        return destination if destination else self.result

    @cached_property
    def false_branch(self):
        if not self.condition:
            return None
        return self.workflow.rule_after(self)

    @cached_property
    def branches(self):
        branches = [self.true_branch]
        if self.false_branch:
            branches.append(self.false_branch)
        return branches

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

    def range_by_condition(self, is_true):
        if is_true:
            return self.true_low_high
        else:
            return self.false_low_high

    def __repr__(self):
        return f"<Rule workflow={self.workflow.name} {self.input}>"
