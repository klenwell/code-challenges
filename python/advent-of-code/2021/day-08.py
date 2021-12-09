"""
Advent of Code 2021 - Day 08
https://adventofcode.com/2021/day/8

Compare: https://github.com/hyper-neutrino/advent-of-code/blob/main/2021/day8p2.py
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        unique_signal_digits = {
            # digit: signal input segments
            1: 2,
            4: 4,
            7: 3,
            8: 7
        }
        unique_segment_digits = []
        input_signal_lengths = unique_signal_digits.values()

        for values in self.output_values:
            for value in values:
                if len(value) in input_signal_lengths:
                    unique_segment_digits.append(value)
        return len(unique_segment_digits)

    @property
    def second(self):
        output_values = []
        for n, signals in enumerate(self.signal_patterns):
            outputs = self.output_values[n]
            mapped_digits = self.map_signals_to_digits(signals)
            output_value = self.decode_outputs(outputs, mapped_digits)
            output_values.append(output_value)
        return sum(output_values)

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def signal_patterns(self):
        patterns = []
        for line in self.input_lines:
            signals, _ = line.split('|')
            pattern = [p for p in signals.strip().split(' ')]
            patterns.append(pattern)
        return patterns

    @cached_property
    def output_values(self):
        values = []
        for line in self.input_lines:
            _, outputs = line.split('|')
            digits = [d for d in outputs.strip().split(' ')]
            values.append(digits)
        return values

    #
    # Methods
    #
    def decode_outputs(self, outputs, mapped_digits):
        output_digits = []

        for output in outputs:
            for n, code in enumerate(mapped_digits):
                if sorted(code) == sorted(output):
                    output_digits.append(n)
                    break

        return int('{}{}{}{}'.format(*output_digits))

    def map_signals_to_digits(self, _signals):
        mapping = [None] * 10
        signals = _signals.copy()

        a_overlaps_b = lambda outer, inner: len(set(inner) - set(outer)) == 0

        # Digits 1-4 can be identified by num of segments
        mapping[1] = [s for s in signals if len(s) == 2][0]
        mapping[4] = [s for s in signals if len(s) == 4][0]
        mapping[7] = [s for s in signals if len(s) == 3][0]
        mapping[8] = [s for s in signals if len(s) == 7][0]
        signals.remove(mapping[1])
        signals.remove(mapping[4])
        signals.remove(mapping[7])
        signals.remove(mapping[8])

        # Digit 3 has 5 segments and overlaps digit 7
        for signal in signals:
            if len(signal) == 5 and a_overlaps_b(signal, mapping[7]):
                mapping[3] = signal
                signals.remove(signal)

        # Digit 9 has 6 segments and overlaps digit 4
        for signal in signals:
            if len(signal) == 6 and a_overlaps_b(signal, mapping[4]):
                mapping[9] = signal
                signals.remove(signal)

        # Digit 0 has 6 segments and overlaps digit 1
        for signal in signals:
            if len(signal) == 6 and a_overlaps_b(signal, mapping[1]):
                mapping[0] = signal
                signals.remove(signal)

        # Digit 6 is last to have 6 segments
        for signal in signals:
            if len(signal) == 6:
                mapping[6] = signal
                signals.remove(signal)

        # Digit 5 is overlapped by 6
        for signal in signals:
            if a_overlaps_b(mapping[6], signal):
                mapping[5] = signal
                signals.remove(signal)

        # Digit 3 overlaps 7
        for signal in signals:
            if a_overlaps_b(signal, mapping[7]):
                mapping[3] = signal
                signals.remove(signal)

        # Which leaves Digit 2
        mapping[2] = signals.pop()
        assert len(signals) == 0, signals

        return mapping


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
