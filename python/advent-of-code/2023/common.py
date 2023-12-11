"""
Some commonly used constants and methods.

Usage:
from config import INPUT_FILE

To profile:
$ python -m cProfile -s cumtime 2023/day-00.py
"""
from os.path import dirname, join as path_join
from functools import cached_property, reduce
import time
import string
import re


# Common Paths
ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')


# Constants
ALPHA_LOWER = string.ascii_lowercase


# Periodic logger
def info(msg, freq=1):
    # https://stackoverflow.com/q/279561/1093087
    try:
        ts = time.time()
        info.split_time = ts - info.last_ts
    except AttributeError:
        info.split_time = 0
    try:
        info.counter += 1
    except AttributeError:
        info.counter = 0
    if info.counter % freq == 0:
        info.last_ts = ts
        print(f"[info:{info.counter}] ({info.split_time:.3f}) {msg}")
    return info


# Extract Numbers
def extract_numbers(str_value, num_type=int):
    # https://stackoverflow.com/a/63619831/1093087
    rp = r'-?\d+\.?\d*'
    return [num_type(s) for s in re.findall(rp, str_value)]


# Grid
class Grid:
    def __init__(self, input):
        self.input = input.strip()
        self.grid = self.init_grid()

    @cached_property
    def rows(self):
        rows = []
        for line in self.input.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def cols(self):
        cols = []
        for n in range(len(self.rows[0])):
            col = []
            for row in self.rows:
                val = row[n]
                col.append(val)
            cols.append(col)
        return cols

    @cached_property
    def pts(self):
        return list(self.grid.keys())

    @cached_property
    def min_x(self):
        return 0

    @cached_property
    def max_x(self):
        return len(self.rows[0]) - 1

    @cached_property
    def min_y(self):
        return 0

    @cached_property
    def max_y(self):
        return len(self.rows) - 1

    def init_grid(self):
        grid = {}
        for y, row in enumerate(self.rows):
            for x, val in enumerate(row):
                pt = (x, y)
                grid[pt] = val
        return grid

    def neighbors(self, pt):
        pts = []
        deltas = [  # Clockwise from NW to W
            (-1, -1), (0, -1), (1, -1), (1, 0),
            (1, 1), (0, 1), (-1, 1), (-1, 0)
        ]
        x, y = pt

        for dx, dy in deltas:
            nx = x + dx
            ny = y + dy

            if (self.min_x <= nx <= self.max_x) and (self.min_y <= ny <= self.max_y):
                npt = (nx, ny)
                pts.append(npt)

        return pts

    def cardinal_neighbors(self, pt):
        # N, S, E, W
        pts = []
        deltas = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        x, y = pt

        for dx, dy in deltas:
            nx = x + dx
            ny = y + dy

            if (self.min_x <= nx <= self.max_x) and (self.min_y <= ny <= self.max_y):
                npt = (nx, ny)
                pts.append(npt)

        return pts


# Compute Facts: 12 = 1,2,3,4,6,12
# Source: https://stackoverflow.com/a/6800214/1093087
def compute_factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
