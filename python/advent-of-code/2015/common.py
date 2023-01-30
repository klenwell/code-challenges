"""
Some commonly used constants and methods.

Usage:
from config import INPUT_FILE

To profile:
$ python -m cProfile -s cumtime 2015/day-00.py
"""
from os.path import dirname, join as path_join


ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
