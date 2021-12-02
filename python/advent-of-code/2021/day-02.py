"""
Advent of Code 2021 - Day 02
https://adventofcode.com/2021/day/2

## PUZZLE
Your horizontal position and depth both start at 0. The steps above would then modify
them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15 and a
depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the
planned course. What do you get if you multiply your final horizontal position by
your final depth?
"""
from os.path import dirname, join as path_join

ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-02.txt')


def extract_movements():
    with open(INPUT_FILE) as file:
        entries = file.readlines()
        return [e.strip() for e in entries]


def track_movements(movements):
    horizontal = 0
    depth = 0

    for movement in movements:
        dir, unit = movement.split(' ')
        unit = int(unit)

        if dir == 'forward':
            horizontal += unit
        elif dir == 'down':
            depth += unit
        elif dir == 'up':
            depth -= unit
        else:
            raise ValueError(dir, unit)

    return horizontal, depth


def track_movements_with_aim(movements):
    horizontal = 0
    depth = 0
    aim = 0

    for movement in movements:
        dir, unit = movement.split(' ')
        unit = int(unit)

        if dir == 'forward':
            horizontal += unit
            depth += unit * aim
        elif dir == 'down':
            aim += unit
        elif dir == 'up':
            aim -= unit
        else:
            raise ValueError(dir, unit)

    return horizontal, depth


def solve_pt1():
    movements = extract_movements()
    horizontal, depth = track_movements(movements)
    return horizontal * depth


def solve_pt2():
    """https://adventofcode.com/2021/day/2#part2"""
    movements = extract_movements()
    horizontal, depth = track_movements_with_aim(movements)
    return horizontal * depth


#
# Main
#
solution = solve_pt1()
print("pt 1 solution: {}".format(solution))

solution = solve_pt2()
print("pt 2 solution: {}".format(solution))
