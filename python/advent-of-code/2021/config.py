"""
Some commonly used values.

Usage:
from config import INPUT_FILE
"""
from os.path import dirname, join as path_join


ROOT_DIR = dirname(__file__)
INPUT_DIR = path_join(ROOT_DIR, 'inputs')
