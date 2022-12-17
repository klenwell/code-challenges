"""
Advent of Code 2022 - Day 15
https://adventofcode.com/2022/day/15
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import re


INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')

TEST_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


class Sensor:
    @staticmethod
    def deploy_all(input):
        sensors = []
        readings = input.split('\n')
        for reading in readings:
            sensor = Sensor(reading)
            sensors.append(sensor)
        return sensors

    def __init__(self, reading):
        self.reading = reading

    @cached_property
    def pt(self):
        sensor_log, _ = self.reading.split(':')
        digits = [int(d) for d in re.findall(r'-?\d+', sensor_log)]
        return (digits[0], digits[1])

    @cached_property
    def beacon_pt(self):
        _, beacon_log = self.reading.split(':')
        digits = [int(d) for d in re.findall(r'-?\d+', beacon_log)]
        return (digits[0], digits[1])

    @cached_property
    def beacon_dist(self):
        # Manhattan distance
        dx = abs(self.beacon_pt[0] - self.x)
        dy = abs(self.beacon_pt[1] - self.y)
        return dx + dy

    @cached_property
    def x(self):
        return self.pt[0]

    @cached_property
    def y(self):
        return self.pt[1]

    @cached_property
    def x_min(self):
        return self.x - self.beacon_dist

    @cached_property
    def x_max(self):
        return self.x + self.beacon_dist

    @cached_property
    def y_min(self):
        return self.y - self.beacon_dist

    @cached_property
    def y_max(self):
        return self.y + self.beacon_dist

    @cached_property
    def y_range(self):
        return range(self.y_min, self.y_max)

    def range_at_row(self, y):
        if y not in self.y_range:
            return set()

        dy = abs(y - self.y)
        x_width = self.beacon_dist - dy
        x_min = self.x - x_width
        x_max = self.x + x_width + 1
        return set(range(x_min, x_max))

    def __repr__(self):
        return '<Sensor pt={} beacon={} dist={}>'.format(
            self.pt, self.beacon_pt, self.beacon_dist)



class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        target_row = 10
        sensors = Sensor.deploy_all(TEST_INPUT)

        # Tests
        test_sensor = sensors[6]
        test_sensor_range = test_sensor.range_at_row(target_row)
        assert test_sensor_range == set(range(2, 15)), test_sensor_range
        assert sensors[0].beacon_pt[0] == -2, sensors[0].beacon_pt[0]

        # Solve
        dead_spots = set()
        beacon_spots = set()

        for sensor in sensors:
            dead_spots = dead_spots.union(sensor.range_at_row(target_row))

            beacon_y = sensor.beacon_pt[1]
            if beacon_y == target_row:
                beacon_spots.add(beacon_y)

        dead_spots = dead_spots - beacon_spots
        return len(dead_spots)

    @property
    def first(self):
        target_row = 2000000
        sensors = Sensor.deploy_all(self.file_input)

        min_x = min(s.x_min for s in sensors)
        max_x = max(s.x_max for s in sensors)
        print(min_x, max_x, max_x - min_x)

        dead_spots = set()
        beacon_spots = set()

        for sensor in sensors:
            sensor_dead_spots = sensor.range_at_row(target_row)
            dead_spots = dead_spots.union(sensor_dead_spots)
            print(sensor.x_min, sensor.x, sensor.x_max, len(sensor_dead_spots))

            beacon_y = sensor.beacon_pt[1]
            if beacon_y == target_row:
                beacon_spots.add(beacon_y)

        dead_spots = dead_spots - beacon_spots
        return len(dead_spots)
        #5716882

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
