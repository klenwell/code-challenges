"""
Some commonly used constants and methods.

Usage:
from config import INPUT_FILE

To profile:
$ python -m cProfile -s cumtime 2015/day-00.py
"""
from os.path import dirname, join as path_join


# Common Paths
ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')


# Periodic logger
def info(msg, freq):
    # https://stackoverflow.com/q/279561/1093087
    try:
        info.counter += 1
    except AttributeError:
        info.counter = 0
    if info.counter % freq == 0:
        print(f"[info:{info.counter}] {msg}")
