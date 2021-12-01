"""
Advent of Code 2021 - Day 01
https://adventofcode.com/2021/day/1

## PUZZLE
The first order of business is to figure out how quickly the depth increases, just so
you know what you're dealing with - you never know if the keys will get carried into
deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the previous
measurement. (There is no measurement before the first measurement.) In the example
above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)

In this example, there are 7 measurements that are larger than the previous measurement.

How many measurements are larger than the previous measurement?
"""
from os.path import dirname, join as path_join

ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')


def extract_measurements():
    with open(INPUT_FILE) as file:
        entries = file.readlines()
        return [int(e) for e in entries]

def count_larger_measurements(measurements):
    count = 0
    previous_measurement = None

    for measurement in measurements:
        if previous_measurement and measurement >= previous_measurement:
            count += 1

        previous_measurement = measurement

    return count


def solve_pt1():
    measurements = extract_measurements()
    print("{} measurements".format(len(measurements)))
    return count_larger_measurements(measurements)


def solve_pt2():
    pass


#
# Main
#
solution = solve_pt1()
print("pt 1 solution: {}".format(solution))

solution = solve_pt2()
print("pt 2 solution: {}".format(solution))
