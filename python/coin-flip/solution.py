"""
Question:

Two people, Alice and Bob, are each flipping a coin repeatedly. Alice will stop
when she flips two heads in a row (HH). Bob will stop when he flips a head
followed immediately by a tail (HT).

Who will flip the coin more times on average: Alice, Bob, or is there no
difference?

Source: https://www.metafilter.com/147228/You-blew-it-and-you-blew-it-big#5945177
"""
import random


COIN_SIDES = ['H', 'T']


def flip_coin():
    return random.choice(COIN_SIDES)


if __name__ == "__main__":
    flips = [flip_coin() for n in range(100)]
    breakpoint()
