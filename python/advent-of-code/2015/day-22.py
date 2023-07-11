"""
Advent of Code 2015 - Day 22
https://adventofcode.com/2015/day/22
"""
from os.path import join as path_join
from functools import cached_property
import math

from common import INPUT_DIR, info


SPELLS = [
    # Name, Cost, Duration, Damage, Defense, Heal, Recharge
    ('Magic Missle', 53, 1, 4, 0, 0, 0),
    ('Drain',        73, 1, 2, 0, 2, 0),
    ('Shield',      113, 6, 0, 7, 0, 0),
    ('Poison',      173, 6, 3, 0, 0, 0),
    ('Recharge',    229, 5, 0, 0, 0, 101)
]


class DeadWizard(Exception): pass


class Wizard:
    def __init__(self, hp, mana, book):
        self.hp = hp
        self.mana = mana
        self.book = book
        self.effects = []
        self.mana_spent = 0
        self.foe = None

    @property
    def damage(self):
        return sum([s.damage for s in self.effects])

    @property
    def defense(self):
        return sum([s.defense for s in self.effects])

    @property
    def died(self):
        return self.hp <= 0

    @property
    def spell_options(self):
        spells = []
        names = set(self.book.names)
        in_effect = set([e.name for e in self.effects])
        options = names - in_effect

        for name in options:
            spell = self.book.read(name)
            if spell.cost <= self.mana:
                spells.append(spell)

        return spells

    def spend_least_mana_to_defeat(self, foe):
        winner = None
        self.foe = foe
        queue = [self]

        while queue:
            #info([w.foe.hp for w in queue], 1000)
            wizard = queue.pop()
            clones = wizard.branch_clones(winner)

            for clone in clones:
                if clone.died:
                    pass
                elif clone.foe.died:
                    if not winner:
                        winner = clone
                    elif clone.mana_spent < winner.mana_spent:
                        winner = clone
                    queue = [c for c in queue if c.mana_spent < winner.mana_spent]
                elif winner and clone.mana_spent < winner.mana_spent:
                    queue.append(clone)
                else:
                    queue.append(clone)

            info(f"DFS: {len(queue)} {winner} {clone} {clone.foe}", 1000)

            queue.sort(key=lambda w: w.foe.hp, reverse=True)

        return winner

    def branch_clones(self, winner):
        clones = []
        for spell in self.spell_options:
            if winner and winner.mana_spent <= self.mana_spent + spell.cost:
                continue
            clone = self.clone()
            clone.battle_round(spell)
            clones.append(clone)
        return clones

    def battle_round(self, spell):
        self.cast_spell(spell)
        self.apply_spell_effects(self.foe)
        self.foe.attacks(self)
        return self

    def cast_spell(self, spell):
        # raise error if spell already in effect
        if spell in self.effects:
            raise ValueError(f"Spell {spell} should not have been an option.")

        # add spell to effects
        self.effects.append(spell)
        self.mana -= spell.cost
        self.mana_spent += spell.cost
        #print(spell.cost, self.mana_spent)

    def apply_spell_effects(self, foe):
        # heal self
        self.hp += sum([s.heal for s in self.effects])

        # recharge self
        self.mana += sum([s.recharge for s in self.effects])

        # attack foe
        self.attacks(foe)

        # tick
        for spell in self.effects:
            spell.tick()

        # clear expired spells
        self.effects = [e for e in self.effects if not e.expired]

    def attacks(self, foe):
        damage = self.damage - foe.defense
        damage = max(damage, 1)
        foe.hp -= damage
        return foe

    def clone(self):
        foe = Boss(self.foe.hp, self.foe.damage)
        clone = Wizard(self.hp, self.mana, self.book)
        clone.effects = [e.clone() for e in self.effects]
        clone.foe = foe
        clone.mana_spent = self.mana_spent
        return clone

    def __repr__(self):
        return f"<Wizard hp={self.hp} mana={self.mana} spent={self.mana_spent}>"


class Boss(Wizard):
    def __init__(self, hp, damage):
        super().__init__(hp, math.inf, None)
        self.attack_damage = damage

    @property
    def damage(self):
        return self.attack_damage

    @property
    def defense(self):
        return 0


class Spell:
    def __init__(self, name, effects):
        self.name = name
        self.effects = effects
        self.ticks = 0

    def clone(self):
        spell = Spell(self.name, self.effects)
        spell.ticks = self.ticks
        return spell

    @cached_property
    def cost(self):
        return self.effects[0]

    @cached_property
    def duration(self):
        return self.effects[1]

    @cached_property
    def damage(self):
        return self.effects[2]

    @cached_property
    def defense(self):
        return self.effects[3]

    @cached_property
    def heal(self):
        return self.effects[4]

    @cached_property
    def recharge(self):
        return self.effects[5]

    @property
    def expired(self):
        return self.ticks >= self.duration

    def tick(self):
        self.ticks += 1


class SpellBook:
    def __init__(self, spells):
        self.spells = spells

    @cached_property
    def index(self):
        index = {}
        for spell in self.spells:
            name = spell[0]
            effects = spell[1:]
            index[name] = effects
        return index

    @cached_property
    def names(self):
        return list(self.index.keys())

    def read(self, name):
        effects = self.index[name]
        return Spell(name, effects)



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
        wizard_book = SpellBook(SPELLS)
        boss_hp = 55
        boss_damage = 8

        wizard = Wizard(wizard_hp, wizard_mana, wizard_book)
        boss = Boss(boss_hp, boss_damage)

        wizard = wizard.spend_least_mana_to_defeat(boss)
        assert wizard.mana_spent < 1212, f"{wizard.mana_spent} is too high"
        return wizard.mana_spent

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
