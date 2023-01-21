"""
Advent of Code 2022 - Day 22 - Monkey Map
https://adventofcode.com/2022/day/22

Map of cube in Part Two test example.
"""
from models.monkey_map.grove_map import GroveMap


class TestCubeMap(GroveMap):
    def map_edges(self, edge1, edge2):
        return dict(zip(range(*edge1), range(*edge2)))

    def wrap_around(self, facing, pt):
        x, y = pt

        # Side 1^ to 2^
        if y == 0 and facing == '^':
            x_map = self.map_edges((8, 11), (3, -1, -1))
            nx = x_map[x]
            ny = 4
            nf = 'v'

        # Side 1< to 3^
        elif x == 7 and y in range(0, 4) and facing == '<':
            yx_map = self.map_edges((0, 4), (4, 8))
            nx = yx_map[y]
            ny = 4
            nf = 'v'

        # Side 1> to 6>
        elif x == 11 and y in range(0, 4) and facing == '>':
            y_map = self.map_edges((0, 4), (11, 7, -1))
            nx = 15
            ny = y_map[y]
            nf = '<'

        # Side 2^ to 1^
        elif y == 4 and x in range(0, 4) and facing == '^':
            x_map = self.map_edges((0, 4), (3, -1, -1))
            nx = x_map[x]
            ny = 0
            nf = 'v'

        # Side 2< to 6v
        elif x == 0 and y in range(4, 8) and facing == '<':
            yx_map = self.map_edges((4, 8), (15, 11, -1))
            nx = yx_map[x]
            ny = 11
            nf = '^'

        # Side 2v to 5v
        elif y == 7 and x in range(0, 4) and facing == 'v':
            yx_map = self.map_edges((0, 4), (11, 7, -1))
            nx = yx_map[x]
            ny = 11
            nf = '^'

        # Side 3^ to 1<
        elif y == 4 and x in range(4, 8) and facing == '^':
            xy_map = self.map_edges((4, 8), (0, 4))
            nx = 8
            ny = xy_map[x]
            nf = '>'

        # Side 3v to 5<
        elif y == 7 and x in range(4, 8) and facing == 'v':
            xy_map = self.map_edges((4, 8), (11, 7, -1))
            nx = 8
            ny = xy_map[x]
            nf = '>'

        # Side 4> to 6^
        elif x == 11 and y in range(4, 8) and facing == '>':
            yx_map = self.map_edges((4, 8), (15, 11, -1))
            nx = yx_map[y]
            ny = 8
            nf = 'v'

        # Side 5< to 3v
        elif x == 8 and y in range(8, 12) and facing == '<':
            yx_map = self.map_edges((8, 12), (7, 3, -1))
            nx = yx_map[x]
            ny = 7
            nf = '^'

        # Side 5v to 2v
        elif y == 11 and x in range(8, 12) and facing == 'v':
            x_map = self.map_edges((8, 12), (3, -1, -1))
            nx = x_map[x]
            ny = 7
            nf = '^'

        # Side 6^ to 4>
        elif y == 8 and x in range(12, 16) and facing == '^':
            xy_map = self.map_edges((12, 16), (4, 8))
            nx = 11
            ny = xy_map[x]
            nf = '<'

        # Side 6> to 1>
        elif x == 15 and y in range(8, 12) and facing == '>':
            y_map = self.map_edges((8, 12), (3, -1, -1))
            nx = 11
            ny = y_map[y]
            nf = '<'

        # Side 6v to 2<
        elif y == 11 and x in range(12, 16) and facing == 'v':
            xy_map = self.map_edges((12, 16), (7, 3, -1))
            nx = 0
            ny = xy_map[x]
            nf = '>'

        else:
            breakpoint()
            raise Exception(f"Missed wrap case: {(facing, pt)}")

        # print(f"{(x, y, facing)} wraps to {(nx, ny, nf)}")
        return (nx, ny, nf)

    def go(self, tiles):
        steps = {
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0),
            '^': (0, -1)
        }

        for n in range(tiles):
            x, y = self.pt
            dx, dy = steps[self.facing]
            nx, ny = x+dx, y+dy
            facing = self.facing
            next_tile = self.tiles.get((nx, ny))

            if next_tile not in ('.', '#'):
                (nx, ny, facing) = self.wrap_around(self.facing, self.pt)
                next_tile = self.tiles.get((nx, ny))

            if next_tile == '.':
                self.pt = (nx, ny)
                self.facing = facing
                self.footprints.append((self.footprint, next_tile))
            elif next_tile == '#':
                self.pt = (x, y)
                self.footprints.append((self.footprint, next_tile))
                return self.pt  # Hit a wall: stop and return
            else:
                raise Exception('Unexpected tile:', self.pt, (nx, ny), next_tile)

        return self.pt
