import math
from functools import cached_property

from models.day_19.step import RatingStep
from models.day_19.rule import WorkflowRule


class Path:
    def __init__(self, steps):
        self.steps = list(steps)

    @cached_property
    def combos(self):
        return self.end_step.ratings.combos

    @cached_property
    def branches(self):
        new_paths = []

        for step in self.next_steps:
            new_path = self.add_step(step)
            new_paths.append(new_path)

        return new_paths

    @cached_property
    def next_steps(self):
        origin = self.destination

        if self.completed:
            return []
        elif isinstance(origin, WorkflowRule):
            rule = origin

            # True Branch
            destination = rule.true_branch
            ratings = self.end_step.ratings.clone()
            ratings = ratings.apply_rule(rule, True)
            true_step = RatingStep(origin, destination, ratings)
            next_steps = [true_step]

            # False Branch
            if rule.false_branch:
                destination = rule.false_branch
                ratings = self.end_step.ratings.clone()
                ratings = ratings.apply_rule(rule, False)
                false_step = RatingStep(origin, destination, ratings)
                next_steps.append(false_step)
            return next_steps
        else:
            workflow = self.destination
            ratings = self.end_step.ratings.clone()
            step = RatingStep(origin, workflow.first_rule, ratings)
            return [step]

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

    def add_step(self, step):
        steps = self.steps + [step]
        return Path(steps)

    def __repr__(self):
        return f"<Path result={self.destination} steps={self.steps}>"
