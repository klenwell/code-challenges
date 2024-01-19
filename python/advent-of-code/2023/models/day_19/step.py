from functools import cached_property


class RatingStep:
    def __init__(self, origin, destination, ratings):
        self.origin = origin
        self.destination = destination
        self.ratings = ratings

    @cached_property
    def category(self):
        return getattr(self.origin, 'category', None)

    def __repr__(self):
        start = getattr(self.origin, 'id', self.origin)
        end = getattr(self.destination, 'id', self.destination)
        route = f"{start}->{end}"
        return f"<Step {route} category={self.category} ratings={self.ratings.range_values}>"


class Step:
    def __init__(self, origin, destination, counts):
        self.origin = origin
        self.destination = destination
        self.counts = counts

    @cached_property
    def category(self):
        return getattr(self.origin, 'category')

    def __repr__(self):
        start = getattr(self.origin, 'id', self.origin)
        end = getattr(self.destination, 'id', self.destination)
        route = f"{start}->{end}"
        return f"<Step {route} category={self.category} counts={self.counts}>"
