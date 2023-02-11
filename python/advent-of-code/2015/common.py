"""
Some commonly used constants and methods.

Usage:
from config import INPUT_FILE

To profile:
$ python -m cProfile -s cumtime 2015/day-00.py
"""
from os.path import dirname, join as path_join
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


# Extract Numbers
def extract_numbers(str_value, num_type=int):
    # https://stackoverflow.com/a/63619831/1093087
    rp = r'-?\d+\.?\d*'
    return [num_type(s) for s in re.findall(rp, str_value)]
