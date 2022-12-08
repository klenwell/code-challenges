"""
Advent of Code 2022 - Day 7
https://adventofcode.com/2022/day/7

References:

"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-07.txt')

TEST_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


class ElfOS:
    def __init__(self):
        self.root = Dir('/')
        self.cwd = self.root

    @property
    def dirs(self):
        return self.root.dirs

    def parse_commands(self, lines):
        commands = []
        in_ls = False
        group = []

        for line in lines:
            if not line:
                continue

            if line.startswith('$'):
                if line.startswith('$ cd'):
                    in_ls = False
                    if group:
                        commands.append(group)
                        group = []
                    commands.append([line])
                else:  # ls
                    in_ls = True
                    group = [line]
            else:
                group.append(line)

        if in_ls:
            commands.append(group)

        return commands

    def run(self, commands):
        command = commands[0]
        if command.startswith('$ cd'):
            dir_name = command.split(' ')[-1]
            self.cd(dir_name)
        elif command.startswith('$ ls'):
            self.ls(commands[1:])

    def cd(self, name):
        if name == '..':
            self.cwd = self.cwd.parent
        else:
            for child in self.cwd.children:
                if type(child) == Dir and name == child.name:
                    self.cwd = child
                    break
        return self.cwd

    def ls(self, objects):
        for object in objects:
            if object.startswith('dir'):
                name = object.split(' ')[-1]
                self.cwd.add_dir(name)
            else:
                size, name = object.split(' ')
                self.cwd.add_file(name, size)

    def __repr__(self):
        return '<ElfOS root={} cwd={}>'.format(self.root, self.cwd)


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    @property
    def size(self):
        return sum([c.size for c in self.children])

    @property
    def dirs(self):
        dirs = []
        for child in self.children:
            if type(child) == Dir:
                dirs.append(child)
                dirs += child.dirs
        return dirs

    def add_dir(self, name):
        self.children.append(Dir(name, self))

    def add_file(self, name, size):
        file = ElfFile(name, size)
        self.children.append(file)

    def __repr__(self):
        return '<Dir name={} children={} size={}>'.format(self.name, len(self.children), self.size)


class ElfFile:
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)

    def __repr__(self):
        return '<File name={} size={}>'.format(self.name, self.size)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test(self):
        MAX_DIR_SIZE = 100000
        lines = TEST_INPUT.split("\n")

        os = ElfOS()
        commands = os.parse_commands(lines)

        for command in commands:
            os.run(command)

        small_dirs = [d for d in os.dirs if d.size <= MAX_DIR_SIZE]
        return sum([d.size for d in small_dirs])

    @property
    def first(self):
        MAX_DIR_SIZE = 100000

        os = ElfOS()
        commands = os.parse_commands(self.input_lines)

        for command in commands:
            os.run(command)

        small_dirs = [d for d in os.dirs if d.size <= MAX_DIR_SIZE]
        return sum([d.size for d in small_dirs])

    @property
    def second(self):
        TOTAL_DISK_SPACE = 70000000
        UPDATE_SPACE = 30000000

        os = ElfOS()
        commands = os.parse_commands(self.input_lines)

        for command in commands:
            os.run(command)

        unused_space = TOTAL_DISK_SPACE - os.root.size
        needed_space = UPDATE_SPACE - unused_space
        dirs = sorted(os.dirs, key=lambda d: d.size)

        for dir in dirs:
            if dir.size >= needed_space:
                return dir.size

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test solution: {}".format(solution.test))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
