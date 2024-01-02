from functools import cached_property, total_ordering


@total_ordering
class Route:
    def __init__(self, parent, hot_path, key_len):
        self.parent = parent
        self.hot_path = hot_path
        self.key_len = key_len
        self.x, self.y = hot_path[-1].pt
        self.pt_cost = hot_path[-1].heat

    @cached_property
    def pt_key(self):
        # This was a big bottleneck.
        # Thanks to https://advent-of-code.xavd.id/writeups/2023/day/17/ found in solution thread.
        # Making change below cut from over 5 mins to just over 1
        # pts = self.last_n_steps(self.key_len)
        # return (self.end_pt, pts)
        dir = self.approach
        steps_in_row = len(self.hot_path)
        return (self.end_pt, dir, steps_in_row)

    @cached_property
    def total_cost(self):
        return sum([hs.heat for hs in self.hot_spots])

    @cached_property
    def hot_spots(self):
        if not self.parent:
            return self.hot_path
        return self.parent.hot_spots + self.hot_path

    @cached_property
    def pts(self):
        return [h.pt for h in self.hot_spots]

    @cached_property
    def approach(self):
        if not len(self.pts) > 1:
            return None

        last_pt = self.pts[-2]
        lx, ly = last_pt

        dx = self.x - lx
        dy = self.y - ly
        return (dx, dy)

    @cached_property
    def end_pt(self):
        return (self.x, self.y)

    @cached_property
    def prev_pt(self):
        if not self.parent:
            return None
        return self.parent.end_pt

    def reverses_direction(self):
        if not self.parent:
            return False
        return self.prev_pt and self.end_pt

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
