"""
Advent of Code 2023 - Day 4
https://adventofcode.com/2023/day/4
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class ScratchCardPile:
    def __init__(self, input):
        self.input = input

    @cached_property
    def lines(self):
        return self.input.split("\n")

    @property
    def points(self):
        total = 0
        for line in self.lines:
            card = ScratchCard(line)
            total += card.points
        return total

    @property
    def initial_cards(self):
        cards = []
        for line in self.lines:
            card = ScratchCard(line, self)
            cards.append(card)
        return cards

    @property
    def scratched_cards(self):
        return self.quick_scratch_cards(self.initial_cards)

    def quick_scratch_cards(self, cards):
        queue = list(cards)
        scratched = 0

        while len(queue) > 0:
            card = queue.pop()
            scratched += 1
            info(f"{len(queue)} {scratched} {card}", 1000)

            # Winning copies go into queue. Copies that don't, they just get counted.
            queue += card.winning_prize_cards
            scratched += len(card.losing_prize_cards)

        return scratched

    def brute_scratch_cards(self, cards):
        queue = list(cards)
        scratched = []

        while len(queue) > 0:
            card = queue.pop()
            scratched.append(card)
            info(f"{len(queue)} {len(scratched)} {card}", 1000)
            for n in range(card.matches):
                copy_number = card.number + n + 1
                copy_index = copy_number - 1
                copied_card = self.initial_cards[copy_index]
                queue.insert(0, copied_card)

            if len(queue) > 20000:
                raise Exception(f"This isn't working: {len(queue)}")

        return len(scratched)




class ScratchCard:
    def __init__(self, input, pile=None):
        self.input = input
        self.pile = pile

    @cached_property
    def is_winner(self):
        return self.matches > 0

    @cached_property
    def prize_cards(self):
        cards = []
        for n in range(self.matches):
            copy_number = self.number + n + 1
            copy_index = copy_number - 1
            copied_card = self.pile.initial_cards[copy_index]
            cards.append(copied_card)
        return cards

    @cached_property
    def winning_prize_cards(self):
        return [card for card in self.prize_cards if card.is_winner]

    @cached_property
    def losing_prize_cards(self):
        return [card for card in self.prize_cards if not card.is_winner]

    @property
    def number(self):
        left, _ = self.input.split('|')
        left, _ = left.split(':')
        _, number = left.split()
        return int(number)

    @cached_property
    def matches(self):
        if len(set(self.card_numbers)) != len(self.card_numbers):
            raise ValueError(f'duplicate card numbers: {self.card_numbers}')
        matches = set(self.winning_numbers).intersection(set(self.card_numbers))
        return len(matches)

    @property
    def winning_numbers(self):
        left, _ = self.input.split('|')
        _, numbers = left.split(':')
        return [int(n) for n in numbers.strip().split(' ') if n != '']

    @property
    def card_numbers(self):
        _, numbers = self.input.split('|')
        return [int(n) for n in numbers.strip().split(' ') if n != '']

    @property
    def points(self):
        if len(set(self.card_numbers)) != len(self.card_numbers):
            raise ValueError(f'duplicate card numbers: {self.card_numbers}')
        matches = set(self.winning_numbers).intersection(set(self.card_numbers))

        if len(matches) > 0:
            return 2**(len(matches) - 1)
        else:
            return 0

    def __repr__(self):
        return f'<Card #{self.number} matches={self.matches}>'


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')

    TEST_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

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
        pile = ScratchCardPile(input)
        return pile.points

    @property
    def second(self):
        input = self.file_input
        pile = ScratchCardPile(input)

        for card in pile.initial_cards:
            assert card.number == pile.initial_cards[card.number-1].number

        return pile.scratched_cards

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        pile = ScratchCardPile(input)
        assert pile.points == 13
        return 'passed'

    @property
    def test2(self):
        input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
        pile = ScratchCardPile(input)
        assert pile.scratched_cards == 30
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
