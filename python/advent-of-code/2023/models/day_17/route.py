from functools import cached_property, total_ordering


@total_ordering
class Route:
    def __init__(self, parent, end_pt, pt_cost):
        self.parent = parent
        self.x, self.y = end_pt
        self.pt_cost = int(pt_cost)

    @cached_property
    def pt_key(self):
        return (self.end_pt, self.last_three_steps)

    @cached_property
    def approach(self):
        if not self.parent:
            return None

        dx = self.x - self.parent.x
        dy = self.y - self.parent.y
        return (dx, dy)

    @cached_property
    def end_pt(self):
        return (self.x, self.y)

    @cached_property
    def total_cost(self):
        if not self.parent:
            return self.pt_cost
        return self.parent.total_cost + self.pt_cost

    @cached_property
    def pts(self):
        if not self.parent:
            return [self.end_pt]
        return self.parent.pts + [self.end_pt]

    @cached_property
    def prev_pt(self):
        if not self.parent:
            return None
        return self.parent.end_pt

    @cached_property
    def last_three_steps(self):
        return tuple(self.pts[-4:])

    @cached_property
    def last_three_steps_in_same_direction(self):
        if len(self.last_three_steps) < 4:
            return False

        last_xs = set()
        last_ys = set()

        for x, y in self.last_three_steps:
            last_xs.add(x)
            last_ys.add(y)

        return len(last_xs) == 1 or len(last_ys) == 1

    def last_n_steps(self, n):
        start = -1 * n
        return tuple(self.pts[start:])

    def last_n_steps_in_same_direction(self, n):
        last_n_steps = self.last_n_steps(n+1)

        if len(last_n_steps) < n+1:
            return False

        last_xs = set()
        last_ys = set()

        for x, y in last_n_steps:
            last_xs.add(x)
            last_ys.add(y)

        return len(last_xs) == 1 or len(last_ys) == 1


    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __repr__(self):
        return f"<Route pt_key={self.pt_key} steps={len(self.pts)} total_cost={self.total_cost}>"
