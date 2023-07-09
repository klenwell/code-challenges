"""
Advent of Code 2015 - Day 22
https://adventofcode.com/2015/day/22
"""
from os.path import join as path_join
from functools import cached_property
import math

from common import INPUT_DIR


SPELLS = [
    # Name, Cost, Duration, Damage, Defense, Heal, Recharge
    ('Magic Missle', 0, 1, 0, 0, 0, 0),
    ('Drain', 0, 1, 0, 0, 0, 0),
    ('Shield', 0, 1, 0, 0, 0, 0),
    ('Poison', 0, 1, 0, 0, 0, 0),
    ('Recharge', 0, 1, 0, 0, 0, 0)
]


class DeadWizard(Exception): pass


class Wizard:
    def __init__(self, hp, mana, spells):
        self.hp = hp
        self.mana = mana
        self.spells = spells
        self.effects = []
        self.mana_spent = 0

    @property
    def damage(self): pass

    @property
    def defense(self): pass

    @property
    def spell_options(self):
        options = set(self.spells) - set(self.effects)
        return [spell for spell in spell_options if spell.cost <= self.mana]

    def battles(self, foe):
        info(f"{self} vs {foe}", 20)
        for n in range(math.inf):
            try:
                self.chooses_spell()
                self.apply_spell_effects(foe)
                foe.chooses_spell()
                foe.apply_spell_effects(self)
            except DeadWizard:
                is_winner = not self.is_dead()
        return is_winner

    def apply_spell_effects(self):
        pass

    def attacks(self, foe):
        if self.is_dead():
            raise DeadWizard(self)
        damage = self.damage - foe.defense
        damage = max(damage, 1)
        foe.hp = foe.hp - damage
        return foe


class Spell:
    @staticmethod
    def types():
        types = {}
        for spell in SPELLS:
            name = spell[0]
            attrs = spells[1:]
            types[name] = attrs
        return types

    @staticmethod
    def init_by_name(name):
        attrs = Spell.types[name]
        return Spell(name, attrs)

    @staticmethod
    def init_attack(name, damage):
        attrs = (0, 1, damage, 0, 0, 0)
        return Spell(name, attrs)

    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs
        self.turns = 0

    @cached_property
    def cost(self):
        return self.attrs[0]

    @cached_property
    def duration(self):
        return self.attrs[1]

    @cached_property
    def damage(self):
        return self.attrs[2]

    @cached_property
    def defense(self):
        return self.attrs[3]

    @cached_property
    def heal(self):
        return self.attrs[4]

    @cached_property
    def recharge(self):
        return self.attrs[5]

    @property
    def is_active(self):
        return self.turns < self.duration


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-22.txt')

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
        wizard_hp = 50
        wizard_mana = 500
        boss_hp = 55
        boss_damage = 8
        boss_spell = Spell.init_attack('Boss Attack', boss_damage)

        wizard = Wizard(wizard_hp, wizard_mana, Spell.types)
        boss = Wizard(boss_hp, math.inf, [boss_spell])

        mana_spent = wizard.spend_least_mana_to_win(boss)
        return mana_spent

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        print(input)
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
