"""
Advent of Code 2015 - Day 21
https://adventofcode.com/2015/day/21
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Character:
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def attacks(self, defender):
        if self.is_dead():
            raise DeadCharacter(self)
        damage = self.damage - defender.armor
        damage = max(damage, 1)
        defender.hp = defender.hp - damage
        return defender

    def is_dead(self):
        return self.hp <= 0

    def __repr__(self):
        return f"<{self.__class__.__name__} hp={self.hp} damage={self.damage} armor={self.armor}>"


class Boss(Character): pass


class Player(Character):
    def __init__(self, hp, damage, armor):
        super().__init__(hp, damage, armor)
        self.spent = 0


class DeadCharacter(Exception): pass



class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-21.txt')

    TEST_INPUT = """\
"""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        battle_over = False
        rounds = 0
        player = Player(8, 5, 5)
        boss = Boss(12, 7, 2)

        while not battle_over:
            rounds += 1
            print(f"Round: {rounds}")
            try:
                player.attacks(boss)
                boss.attacks(player)
                print(player, boss)
            except DeadCharacter as loser:
                print(f"Loser: {loser}")
                battle_over = True

        assert boss.is_dead(), boss
        assert player.hp == 2, player.hp
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
