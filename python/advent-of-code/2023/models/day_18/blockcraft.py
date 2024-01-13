from functools import cached_property
from common import info


DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}


class LavaPit:
    def __init__(self, input):
        self.input = input.strip()
        self.holes = {}

    @cached_property
    def cubic_meters(self):
        self.excavate()
        self.fill()
        return len(self.holes)

    @cached_property
    def instructions(self):
        instructions = []
        lines = self.input.split("\n")
        for line in lines:
            dir, size, code = line.strip().split()
            rgb = code[2:-1]
            instruction = (dir, int(size), rgb)
            instructions.append(instruction)
        return instructions

    def excavate(self):
        hole = Hole(0, 0, None)
        for dir, size, rgb in self.instructions:
            dx, dy = DIRS[dir]
            for n in range(size):
                hole.x += dx
                hole.y += dy
                hole.rgb = rgb
                self.dig_hole(hole)
                info(f"excavating {hole}", 1000)

    def fill(self):
        start_pt = self.find_inner_pt()
        queue = [start_pt]

        while len(queue) > 0:
            x, y = queue.pop()
            hole = Hole(x, y, None)
            self.dig_hole(hole)
            info(f"filling {hole}", 10000)


            for npt in self.neighbors(hole.pt):
                if npt not in self.holes:
                    queue.append(npt)

    def find_inner_pt(self):
        iy = min([y for _,y in self.holes.keys()])
        ix = min([x for x,y in self.holes.keys() if y == iy])
        hole = self.holes.get((ix, iy), False)

        while hole:
            print(hole)
            ix = hole.x + 1
            iy = hole.y + 1
            hole = self.holes.get((ix, iy), False)

        print('start', ix, iy)
        #breakpoint()
        return (ix, iy)

    def neighbors(self, pt):
        x, y = pt
        for dx, dy in DIRS.values():
            yield (x+dx, y+dy)

    def dig_hole(self, hole):
        new_hole = Hole(hole.x, hole.y, hole.rgb)
        self.holes[new_hole.pt] = new_hole


class Hole:
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb

    @property
    def pt(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"<Hole {self.pt} rgb={self.rgb}>"