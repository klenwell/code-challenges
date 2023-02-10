"""
Advent of Code 2015 - Day 15
https://adventofcode.com/2015/day/15

Day 15: Science for Hungry People
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


def permutate_ingredients(num, target, index=0, mixes=None):
    new_mixes = []

    if index == num:
        for mix in mixes:
            if sum(mix) == target:
                new_mixes.append(mix)
        return new_mixes

    if not mixes:
        mix = [0] * num
        for n in range(target):
            new_mix = mix.copy()
            new_mix[index] = n
            new_mixes.append(new_mix)

    else:
        for mix in mixes:
            remainder = target - sum(mix)
            for n in range(remainder+1):
                new_mix = mix.copy()
                new_mix[index] = n
                new_mixes.append(new_mix)

    print(f"{index} {len(new_mixes)}")
    return permutate_ingredients(num, target, index+1, new_mixes)


class SantaCookieAI:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def ingredients(self):
        ingredients = []
        for property_sheet in self.input.split('\n'):
            ingredient = MagicIngredient(property_sheet)
            ingredients.append(ingredient)
        return ingredients

    @cached_property
    def ingredient_mixes(self):
        return permutate_ingredients(len(self.ingredients), 100)

    def optimize_ingredients(self):
        top_score_mix = (0, None)

        for mix_ratio in self.ingredient_mixes:
            mix_score = self.score_mix(mix_ratio)
            if mix_score > top_score_mix[0]:
                top_score_mix = (mix_score, mix_ratio)
            info(top_score_mix, 50000)

        return top_score_mix

    def score_mix(self, mix_ratio):
        score = 1
        properties = ['capacity', 'durability', 'flavor', 'texture']
        prop_scores = dict([(prop, []) for prop in properties])

        for n, tsps in enumerate(mix_ratio):
            ingredient = self.ingredients[n]
            for property in properties:
                value = ingredient.properties[property]
                prop_score = tsps * value
                prop_scores[property].append(prop_score)

        #print(self.ingredients, mix_ratio)
        for prop, scores in prop_scores.items():
            prop_score = sum(scores)
            prop_score = max(prop_score, 0)
            score = score * prop_score
            #print(prop, scores, prop_score)

        return score


class MagicIngredient:
    def __init__(self, property_csv):
        self.property_csv = property_csv
        self.properties = self.parse_properties(property_csv)
        self.name = self.properties['name']

    def parse_properties(self, property_csv):
        properties = {}
        name, props_csv = property_csv.split(': ')
        properties['name'] = name.strip()

        props = props_csv.split(', ')
        for prop_val in props:
            key, value = prop_val.strip().split(' ')
            properties[key] = int(value)

        return properties

    def __repr__(self):
        return f"<{self.name} {self.properties}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')

    TEST_INPUT = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

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
        cookie_ai = SantaCookieAI(input)
        score, mix = cookie_ai.optimize_ingredients()
        print(score, mix)
        return score

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        cookie_ai = SantaCookieAI(input)
        assert cookie_ai.ingredients[0].name == 'Butterscotch', cookie_ai.ingredients[0]
        assert cookie_ai.ingredients[1].name == 'Cinnamon', cookie_ai.ingredients[1]
        assert len(cookie_ai.ingredient_mixes) == 100, len(cookie_ai.ingredient_mixes)

        score = cookie_ai.score_mix((44, 56))
        assert score == 62842880, score

        score, mix = cookie_ai.optimize_ingredients()
        assert score == 62842880, (score, mix)

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
