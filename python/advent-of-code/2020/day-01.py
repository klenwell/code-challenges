"""
Advent of Code 2021 - Day 01
https://adventofcode.com/2020/day/1

## PUZZLE
Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""
from os.path import dirname, join as path_join

ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')

TARGET_SUM = 2020


def extract_entries():
    with open(INPUT_FILE) as file:
        entries = file.readlines()
        return [int(e) for e in entries]

def find_complements(target, entries):
    for entry in entries:
        #print("testing: {} to match {}".format(entry, target))
        for complement in entries:
            if target - entry == complement:
                return (entry, complement)

    return None


def solve_pt1():
    entries = extract_entries()
    (entry1, entry2) = find_complements(TARGET_SUM, entries)
    return entry1 * entry2


def solve_pt2():
    entries = extract_entries()

    for entry in entries:
        partial_target = TARGET_SUM - entry
        complements = find_complements(partial_target, entries)

        if complements:
            (c1, c2) = complements
            return entry * c1 * c2


#
# Main
#
solution = solve_pt1()
print("pt 1 solution: {}".format(solution))

solution = solve_pt2()
print("pt 2 solution: {}".format(solution))
