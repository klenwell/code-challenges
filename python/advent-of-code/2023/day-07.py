"""
Advent of Code 2023 - Day 7
https://adventofcode.com/2023/day/7
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class CamelDealer:
    def __init__(self, input):
        self.input = input

    @cached_property
    def total_winnings(self):
        values = []
        for n, hand in enumerate(self.sorted_hands):
            rank = len(self.sorted_hands) - n
            value = hand.compute_value(rank)
            values.append(value)
        return sum(values)

    @cached_property
    def hands(self):
        hands = []
        for line in self.input.strip().split("\n"):
            cards, bid = line.split(' ')
            hand = CamelHand(cards, bid)
            hands.append(hand)
        return hands

    @cached_property
    def sorted_hands(self):
        return sorted(self.hands, key=lambda h: h.sort_key)


class CamelHand:
    RANKS = [(5,), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1) ]
    CARD_TYPES = list('AKQJT98765432')

    def __init__(self, input, bid):
        self.input = input
        self.bid = int(bid)

    @cached_property
    def cards(self):
        return list(self.input)

    @cached_property
    def card_counts(self):
        # https://stackoverflow.com/a/23909767/1093087
        counts = [self.cards.count(c) for c in set(self.cards)]
        return tuple(sorted(counts, reverse=True))

    @cached_property
    def type_key(self):
        return self.RANKS.index(self.card_counts)

    @cached_property
    def ordering_key(self):
        key = []
        for card in self.cards:
            key.append(self.CARD_TYPES.index(card))
        return tuple(key)

    @cached_property
    def sort_key(self):
        return (self.type_key, self.ordering_key)

    def compute_value(self, rank):
        return self.bid * rank

    def __repr__(self):
        return f"<Hand cards={self.cards} bid={self.bid} sort_key={self.sort_key}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-07.txt')

    TEST_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

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
        dealer = CamelDealer(input)
        return dealer.total_winnings

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT

        hand = CamelHand('KTJJT', 220)
        print(hand)
        assert hand.card_counts == (2, 2, 1), hand
        assert hand.bid == 220, hand

        dealer = CamelDealer(input)
        assert dealer.total_winnings == 6440, dealer.total_winnings
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
