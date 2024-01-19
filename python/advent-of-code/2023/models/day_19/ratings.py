from functools import cached_property
import math
import warnings


MAX_VALUE = 4000


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


class PossibleRatings:
    def __init__(self, x_range, m_range, a_range, s_range):
        self.ranges = {
            'x': x_range,
            'm': m_range,
            'a': a_range,
            's': s_range
        }

    @staticmethod
    def max_ranges():
        ranges = [(1, MAX_VALUE) for n in range(4)]
        return PossibleRatings(*ranges)

    @property
    def range_values(self):
        return list(self.ranges.values())

    @property
    def combos(self):
        return math.prod(list(self.counts.values()))

    @property
    def counts(self):
        counts = {}
        for cat, range in self.ranges.items():
            lo, hi = range
            count = hi - lo + 1
            counts[cat] = max(count, 0)
        return counts

    def apply_rule(self, rule, is_true):
        if condition := not getattr(rule, 'condition', '!rule'):
            if condition == '!rule':
                warnings.warn(f"{rule} is not a rule")
            return self

        low, high = self.ranges[rule.category]
        rule_low, rule_high = rule.range_by_condition(is_true)
        new_lo = max(low, rule_low)
        new_hi = min(high, rule_high)

        self.ranges[rule.category] = (new_lo, new_hi)
        return self.clone()

    def clone(self):
        return PossibleRatings(*self.range_values)

    def __repr__(self):
        return f"<Ratings combos={self.combos} {list(self.ranges.values())}>"
