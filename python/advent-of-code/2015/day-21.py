"""
Advent of Code 2015 - Day 21
https://adventofcode.com/2015/day/21
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info
import itertools


SHOP_INVENTORY = """\
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""


class Character:
    def __init__(self, hp, weapon, armor=None):
        self.hp = hp
        self.weapon = weapon
        self.armor = armor
        self.rings = []

    def outfit(self, kit):
        self.weapon = kit.weapon
        self.armor = kit.armor
        self.rings = kit.rings

    @property
    def kit(self):
        return [self.weapon] + [self.armor] + list(self.rings)

    @property
    def damage(self):
        return sum([item.damage for item in self.kit])

    @property
    def defense(self):
        return sum([item.armor for item in self.kit])

    def battles(self, opponent):
        battle_over = False
        rounds = 0

        info(f"{self} vs {opponent}", 20)

        while not battle_over:
            rounds += 1
            try:
                self.attacks(opponent)
                opponent.attacks(self)
            except DeadCharacter:
                battle_over = True

        is_winner = not self.is_dead()
        return is_winner

    def attacks(self, opponent):
        if self.is_dead():
            raise DeadCharacter(self)
        damage = self.damage - opponent.defense
        damage = max(damage, 1)
        opponent.hp = opponent.hp - damage
        return opponent

    def is_dead(self):
        return self.hp <= 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"<{name} hp={self.hp} damage={self.damage} defense={self.defense}>"


class Kit:
    def __init__(self, items):
        self.items = items
        self.weapon = items[0]
        self.armor = items[1]

        rings = items[2]
        if type(rings) == tuple:
            self.rings = rings
        else:
            self.rings = (rings,)

    @cached_property
    def cost(self):
        rings_cost = sum([r.cost for r in self.rings])
        return self.weapon.cost + self.armor.cost + rings_cost

    def __repr__(self):
        return f"<Kit cost={self.cost} {self.items}>"


class Shop:
    def __init__(self):
        self.inventory = self.parse_inventory(SHOP_INVENTORY)

    @property
    def no_ring(self):
        return Item('Ringless 0 0 0', 'rings')

    @property
    def no_armor(self):
        return Item('Armorless 0 0 0', 'armor')

    @cached_property
    def ring_packs(self):
        rings = self.rings + [self.no_ring]
        ring_combos = itertools.combinations(self.rings, 2)
        return rings + list(ring_combos)

    @cached_property
    def kits(self):
        armors = self.armors + [self.no_armor]
        kits = itertools.product(self.weapons, armors, self.ring_packs)
        return sorted([Kit(kit) for kit in kits], key=lambda k: k.cost)

    @cached_property
    def weapons(self):
        return [good for good in self.inventory if good.dept == 'weapons']

    @cached_property
    def armors(self):
        return [good for good in self.inventory if good.dept == 'armor']

    @cached_property
    def rings(self):
        return [good for good in self.inventory if good.dept == 'rings']

    def parse_inventory(self, inventory):
        goods = []

        for line in inventory.split('\n'):
            if ':' in line:
                name, _ = line.split(':')
                department = name.lower()
                continue
            elif not line.strip():
                continue
            else:
                good = Item(line, department)
                goods.append(good)

        return goods


class Item:
    def __init__(self, line, department):
        traits = line.split()
        self.name = ' '.join(traits[:-3]).lower()
        self.cost = int(traits[-3])
        self.damage = int(traits[-2])
        self.armor = int(traits[-1])
        self.dept = department

    def __repr__(self):
        return f"<Item {self.dept} {self.name}>"


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
        player_hp = 100
        boss_hp = 104
        boss_weapon = Item('Staff 1000 8 1', 'staffs')
        shop = Shop()

        for kit in shop.kits:
            player = Character(player_hp, None, None)
            boss = Character(boss_hp, boss_weapon, shop.no_armor)
            player.outfit(kit)
            player_wins = player.battles(boss)
            if player_wins:
                print(player, kit)
                return kit.cost

    @property
    def second(self):
        player_hp = 100
        boss_hp = 104
        boss_weapon = Item('Staff 1000 8 1', 'staffs')
        shop = Shop()

        for kit in reversed(shop.kits):
            player = Character(player_hp, None, None)
            boss = Character(boss_hp, boss_weapon, shop.no_armor)
            player.outfit(kit)
            player_wins = player.battles(boss)
            if not player_wins:
                print(player, kit)
                return kit.cost

    #
    # Tests
    #
    @property
    def test1(self):
        player_weapon = Item('Wand 100 5 5', 'wands')
        boss_weapon = Item('Wand 100 7 2', 'wands')
        shop = Shop()
        player = Character(8, player_weapon, shop.no_armor)
        boss = Character(12, boss_weapon, shop.no_armor)

        is_winner = player.battles(boss)

        assert boss.is_dead(), boss
        assert player.hp == 2, player.hp
        assert is_winner, player
        return 'passed'

    @property
    def test2(self):
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
