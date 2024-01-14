from functools import cached_property


class Parcel:
    def __init__(self, pts):
        self.pts = pts

    @cached_property
    def area(self):
        return self.width * self.height

    @cached_property
    def mid_pt(self):
        x = (max(self.xs) + min(self.xs)) / 2
        y = (max(self.ys) + min(self.ys)) / 2
        return (x, y)

    @cached_property
    def width(self):
        # Edge case: consider box with pts (0,0) -> (4,0) -> (4,4) -> (0,0). Subtracting
        # coordinates gives you 4x4 when it should be 5x5.
        return max(self.xs) - self.min_x + 1

    @cached_property
    def height(self):
        return max(self.ys) - self.min_y + 1

    @cached_property
    def xs(self):
        return [x for x, _ in self.pts]

    @cached_property
    def ys(self):
        return [y for _, y in self.pts]

    @cached_property
    def min_x(self):
        return min(self.xs)

    @cached_property
    def min_y(self):
        return min(self.ys)

    @cached_property
    def edges(self):
        edges = []
        pts = self.pts + [self.pts[0]]
        for n, pt in enumerate(pts[:-1]):
            next_pt = pts[n+1]
            min_pt, max_pt = sorted([pt, next_pt])
            edge = (min_pt, max_pt)
            edges.append(edge)
        return edges

    def shares_edge_with(self, other):
        return len(set(self.edges).intersection(set(other.edges))) > 0

    def __repr__(self):
        wxh = f"{self.width}x{self.height}"
        pts = sorted(self.pts)
        return f"<Parcel {wxh} {pts} mid_pt={self.mid_pt} area={self.area}>"
