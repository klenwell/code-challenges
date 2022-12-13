"""
Advent of Code 2022 - Day 13
https://adventofcode.com/2022/day/13
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import math


INPUT_FILE = path_join(INPUT_DIR, 'day-13.txt')

TEST_INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


class ElfPacket:
    DIVIDER_PACKET_SIGNALS = ['[[2]]', '[[6]]']

    @staticmethod
    def extract_decoder_key(sorted_packets):
        divider_packet_indexes = []
        for n, packet in enumerate(sorted_packets):
            index = n + 1
            if packet.is_divider():
                divider_packet_indexes.append(index)
        return math.prod(divider_packet_indexes)

    @staticmethod
    def bubble_sort(packets):
        n = len(packets)
        swapped = True

        while swapped:
            swapped = False
            for i in range(n-1):
                left_packet = packets[i]
                right_packet = packets[i+1]
                ordered = left_packet < right_packet

                if not ordered:
                    packets[i], packets[i+1] = right_packet, left_packet
                    swapped = True

        return packets

    @staticmethod
    def parse_signal(distress_signal):
        packet_pairs = []
        message_pairs = [p for p in distress_signal.split('\n\n')]
        for n, message_pair in enumerate(message_pairs):
            index = n + 1
            left_msg, right_msg  = message_pair.split('\n')
            packet_pair = (ElfPacket(left_msg, index), ElfPacket(right_msg, index))
            packet_pairs.append(packet_pair)
        return packet_pairs

    @staticmethod
    def parse_signal_with_divider_packets(distress_signal):
        packets = []

        for div_msg in ElfPacket.DIVIDER_PACKET_SIGNALS:
            packets.append(ElfPacket(div_msg))

        packet_pairs = ElfPacket.parse_signal(distress_signal)
        for left_packet, right_packet in packet_pairs:
            packets.append(left_packet)
            packets.append(right_packet)

        return packets

    def __init__(self, message, index=None):
        self.message = message
        self.data = eval(message)
        self.index = index

    def __lt__(self, other):
        return self.compare_lists(self.data, other.data)

    def is_divider(self):
        return self.message in ElfPacket.DIVIDER_PACKET_SIGNALS

    def compare_lists(self, left_list, right_list):
        for n, left_input in enumerate(left_list):
            try:
                right_input = right_list[n]
            except IndexError:
                return False

            if type(left_input) == int and type(right_input) == int:
                if left_input < right_input:
                    return True
                elif left_input > right_input:
                    return False

            elif type(left_input) == int and type(right_input) == list:
                ordered = self.compare_lists([left_input], right_input)
                if ordered is not None:
                    return ordered

            elif type(left_input) == list and type(right_input) == int:
                ordered = self.compare_lists(left_input, [right_input])
                if ordered is not None:
                    return ordered

            else:
                ordered = self.compare_lists(left_input, right_input)
                if ordered is not None:
                    return ordered

        if len(right_list) > len(left_list):
            return True

        return None

    def __repr__(self):
        return '<Packet data={}>'.format(self.data)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        ordered_packets = []
        distress_signal = TEST_INPUT
        packet_pairs = ElfPacket.parse_signal(distress_signal)

        for left_packet, right_packet in packet_pairs:
            # print(left_packet.index, left_packet < right_packet)
            if left_packet < right_packet:
                ordered_packets.append(left_packet)

        return sum([packet.index for packet in ordered_packets])

    @property
    def first(self):
        ordered_packets = []
        distress_signal = self.file_input
        packet_pairs = ElfPacket.parse_signal(distress_signal)

        for left_packet, right_packet in packet_pairs:
            if left_packet < right_packet:
                ordered_packets.append(left_packet)

        return sum([packet.index for packet in ordered_packets])

    @property
    def test2(self):
        distress_signal = TEST_INPUT
        packets = ElfPacket.parse_signal_with_divider_packets(distress_signal)
        sorted_packets = ElfPacket.bubble_sort(packets)
        return ElfPacket.extract_decoder_key(sorted_packets)

    @property
    def second(self):
        distress_signal = self.file_input
        packets = ElfPacket.parse_signal_with_divider_packets(distress_signal)
        sorted_packets = ElfPacket.bubble_sort(packets)
        return ElfPacket.extract_decoder_key(sorted_packets)

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
