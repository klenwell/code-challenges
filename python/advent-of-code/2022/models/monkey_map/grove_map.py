"""
Advent of Code 2022 - Day 22 - Monkey Map
https://adventofcode.com/2022/day/22

2d map for Part One of problem.
"""
from functools import cached_property


class GroveMap:
    def __init__(self, input):
        self.input = input
        self.pt = self.starting_pt
        self.facing = '>'
        self.footprints = []

    @property
    def x(self):
        return self.pt[0]

    @property
    def y(self):
        return self.pt[1]

    @property
    def col(self):
        return self.x + 1

    @property
    def row(self):
        return self.y + 1

    @property
    def footprint(self):
        return (self.facing, self.pt)

    @cached_property
    def tiles(self):
        tiles = {}
        for y, row in enumerate(self.rows):
            for x, tile in enumerate(row):
                tiles[(x, y)] = tile
        return tiles

    @cached_property
    def pts(self):
        return list(self.tiles.keys())

    @cached_property
    def tiled_pts(self):
        return [pt for pt in self.pts if self.tiles[pt] in ('.', '#')]

    @cached_property
    def rows(self):
        rows = []
        for line in self.input.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def starting_pt(self):
        x = next(n for n, x in enumerate(self.rows[0]) if x == '.')
        y = 0
        return (x, y)

    def move(self, movement):
        # start_pt = str(self)
        rotation, tiles = movement
        self.facing = self.rotate(self.facing, rotation)
        self.pt = self.go(tiles)
        # print('move', start_pt, movement, self)
        return self.pt

    def go(self, tiles):
        steps = {
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0),
            '^': (0, -1)
        }

        step = steps[self.facing]

        for n in range(tiles):
            x, y = self.pt
            dx, dy = step
            nx, ny = x+dx, y+dy
            next_tile = self.tiles.get((nx, ny))

            if next_tile not in ('.', '#'):
                (nx, ny) = self.wrap_around(self.facing, self.pt)
                next_tile = self.tiles.get((nx, ny))

            if next_tile == '.':
                self.pt = (nx, ny)
                self.footprints.append((self.footprint, next_tile))
            elif next_tile == '#':
                self.pt = (x, y)
                self.footprints.append((self.footprint, next_tile))
                return self.pt  # Hit a wall: stop and return
            else:
                raise Exception('Unexpected tile:', self.pt, (nx, ny), next_tile)

        return self.pt

    def wrap_around(self, facing, pt):
        # If a movement instruction would take you off of the map, you wrap around to the other
        # side of the board. In other words, if your next tile is off of the board, you should
        # instead look in the direction opposite of your current facing as far as you can until
        # you find the opposite edge of the board, then reappear there.
        valid_tiles = ('.', '#')
        tiles = self.tiles

        if facing == '>':
            row_pts = [pt for pt in self.pts if pt[1] == self.pt[1] and tiles[pt] in valid_tiles]
            next_pt = sorted(row_pts, key=lambda pt: pt[0])[0]
        elif facing == '<':
            row_pts = [pt for pt in self.pts if pt[1] == self.pt[1] and tiles[pt] in valid_tiles]
            next_pt = sorted(row_pts, key=lambda pt: pt[0])[-1]
        elif facing == '^':
            col_pts = [pt for pt in self.pts if pt[0] == self.pt[0] and tiles[pt] in valid_tiles]
            next_pt = sorted(col_pts, key=lambda pt: pt[0])[-1]
        else:  # == 'v'
            col_pts = [pt for pt in self.pts if pt[0] == self.pt[0] and tiles[pt] in valid_tiles]
            next_pt = sorted(col_pts, key=lambda pt: pt[0])[0]

        return next_pt

    def rotate(self, facing, rotation):
        seqs = {
            'L': '>^<v',
            'R': '>v<^'
        }

        seq = seqs.get(rotation)

        if not seq:
            return facing

        # Rotate to current spot
        q = list(seq)
        dir = q.pop(0)
        while dir != facing:
            q.append(dir)
            dir = q.pop(0)

        # New facing direction will be next in queue
        # print(f'rotate {rotation} from {facing} to {q[0]}')
        return q[0]

    def __repr__(self):
        return f"<MonkeyMap pt={self.pt} facing=({self.facing})>"
