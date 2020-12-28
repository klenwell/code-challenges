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


def flip_coin_until(goal, max_flips=1000):
    """goal should desired sequence of flips. E.g. ["H", "T"]

    Returns complete sequence once goal is met. Or raises error if too many flips.
    """
    flips = []
    goal_len = len(goal)
    max_flips = 1000

    for n in range(max_flips):
        flip = flip_coin()
        flips.append(flip)
        recent_flips = flips[-len(goal):]

        if recent_flips == goal:
            return flips

    # Should not get here.
    raise ValueError("Too many flips: {}".format(len(flips)))


if __name__ == "__main__":
    flip_seqs = [flip_coin_until(["H", "H", "H"]) for n in range(10)]
    breakpoint()
