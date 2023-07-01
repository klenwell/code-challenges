"""
Advent of Code 2015 - Day 21
https://adventofcode.com/2015/day/21

Next Step: shop packages all possible kits
kit = 1 weapon, 0 or 1 armor, 0 to 2 rings
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR
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

    def battles(self, defender):
        battle_over = False
        rounds = 0

        print(f"{self} vs {defender}")

        while not battle_over:
            rounds += 1
            print(f"Round: {rounds}")
            try:
                self.attacks(defender)
                defender.attacks(self)
                print(f"({rounds}) {self} {defender}")
            except DeadCharacter as loser:
                print(f"{loser} loses!")
                battle_over = True

        is_winner = not self.is_dead()
        return is_winner

    def attacks(self, defender):
        if self.is_dead():
            raise DeadCharacter(self)
        damage = self.damage - defender.defense
        damage = max(damage, 1)
        defender.hp = defender.hp - damage
        return defender

    def shop_for_upgrade(self, shop):
        # find cheapest upgrade
        weapon_upgrade = self.upgrade_weapon(shop)
        armor_upgrade = self.upgrade_armor(shop)
        ring_upgrade = self.upgrade_ring(shop)
        upgrades = [weapon_upgrade, armor_upgrade, ring_upgrade]
        return sort(upgrades, key=lambda u: u.cost)[0]

    def upgrade(self, upgrade):
        if upgrade.dept == 'weapons':
            self.weapon = upgrade.new
        elif upgrade.dept == 'armor':
            self.armor = upgrade.new
        elif upgrade.dept == 'rings':
            self.rings = upgrade.new

        self.spent += upgrade.new.cost


    def upgrade_weapon(self, shop):
        weapons = sorted(shop.weapons, key=lambda w: w.cost)
        for weapon in weapons:
            if weapon.cost > self.weapon:
                return Upgrade(weapon, self.weapon)

    def upgrade_armor(self, shop):
        armors = sorted(shop.armors, key=lambda a: a.cost)
        for armor in armors:
            if armor.cost > self.armor:
                return Upgrade(armor, self.armor)

    def upgrade_left_ring(self, shop):
        available_rings = list(set(shop.rings) - set(self.rings))
        rings = sorted(available_rings, key=lambda r: r.cost)
        for ring in rings:
            if ring.cost > self.left_ring:
                return Upgrade(armor, self.left_ring)

    def upgrade_right_ring(self, shop):
        pass

    def is_dead(self):
        return self.hp <= 0

    def __repr__(self):
        name = self.__class__.__name__
        return f"<{name} hp={self.hp} damage={self.damage} defense={self.defense}>"


class Boss(Character): pass


class Player(Character):
    def __init__(self, hp, weapon, armor=None):
        super().__init__(hp, weapon, armor)
        self.spent = 0


class ShopKit:
    def __init__(self, items):
        self.items = items
        self.weapon = items[0]
        self.armor = items[1]

        rings = items[2]
        if type(rings) == tuple:
            self.rings = rings
        else:
            self.rings = (rings,)

        print(self.rings)

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
        return ShopGood('Ringless 0 0 0', 'rings')

    @property
    def no_armor(self):
        return ShopGood('Armorless 0 0 0', 'armor')

    @cached_property
    def ring_packs(self):
        rings = self.rings + [self.no_ring]
        ring_combos = itertools.combinations(self.rings, 2)
        return rings + list(ring_combos)

    @cached_property
    def kits(self):
        armors = self.armors + [self.no_armor]
        kits = itertools.product(self.weapons, armors, self.ring_packs)
        return sorted([ShopKit(kit) for kit in kits], key=lambda k: k.cost)

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
                    good = ShopGood(line, department)
                    goods.append(good)

        return goods


class Upgrade:
    def __init__(self, new, old=None):
        if not old:
            old = ShopGood('Nothing  0  0  0', new.dept)
        self.new = new
        self.old = old

    @property
    def cost(self):
        return self.new.cost - self.old.cost

    @property
    def benefit(self):
        return (self.new.damage - self.old.damage) + (self.new.armor - self.old.armor)

    @property
    def dept(self):
        return self.new.dept


class ShopGood:
    def __init__(self, line, department):
        traits = line.split()
        self.name = ' '.join(traits[:-3]).lower()
        self.cost = int(traits[-3])
        self.damage = int(traits[-2])
        self.armor = int(traits[-1])
        self.dept = department

    def __repr__(self):
        return f"<ShopGood {self.dept} {self.name}>"



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
        boss_weapon = ShopGood('Staff 1000 8 1', 'staffs')
        shop = Shop()

        for kit in shop.kits:
            player = Player(player_hp, None, None)
            boss = Boss(boss_hp, boss_weapon, shop.no_armor)
            player.outfit(kit)
            player_wins = player.battles(boss)
            if player_wins:
                print(player, player.kit)
                return kit.cost

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        shop = Shop()
        print(shop.kits)
        print(len(shop.ring_packs), len(shop.kits))
        player_weapon = ShopGood('Wand 100 5 5', 'wands')
        boss_weapon = ShopGood('Wand 100 7 2', 'wands')
        player = Player(8, player_weapon, shop.no_armor)
        boss = Boss(12, boss_weapon, shop.no_armor)

        is_winner = player.battles(boss)

        assert boss.is_dead(), boss
        assert player.hp == 2, player.hp
        assert is_winner, player
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
