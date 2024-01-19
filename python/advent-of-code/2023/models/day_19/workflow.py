from functools import cached_property
from models.day_19.rule import WorkflowRule


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
    def first_rule(self):
        return self.rules[0]

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
