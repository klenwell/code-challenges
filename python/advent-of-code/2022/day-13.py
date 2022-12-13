"""
Advent of Code 2022 - Day 13
https://adventofcode.com/2022/day/13
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


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
    def __init__(self, message, index=None):
        self.data = eval(message)
        self.index = index

    def compare_right_packet(self, right_packet):
        #print('compare_packets', self, right_packet)
        return self.compare_lists(self.data, right_packet.data)

    def compare_lists(self, left_list, right_list):
        #print('compare_lists', left_list, right_list)
        for n, left_input in enumerate(left_list):
            try:
                right_input = right_list[n]
            except IndexError:
                return False

            if type(left_input) == int and type(right_input) == int:
                #print('compare', left_input, right_input)
                if left_input < right_input:
                    return True
                elif left_input > right_input:
                    return False

            elif type(left_input) == int and type(right_input) == list:
                ordered = self.compare_lists([left_input], right_input)
                if ordered != None:
                    return ordered

            elif type(left_input) == list and type(right_input) == int:
                ordered = self.compare_lists(left_input, [right_input])
                if ordered != None:
                    return ordered

            else:
                ordered = self.compare_lists(left_input, right_input)
                if ordered != None:
                    return ordered

        if len(right_list) > len(left_list):
            return True

        return None

    def __repr__(self):
        return '<Packet data={}>'.format(self.data)


def sort_packets(packets):
    n = len(packets)
    swapped = True

    while swapped:
        swapped = False
        for i in range(n-1):
            left_packet = packets[i]
            right_packet = packets[i+1]
            ordered = left_packet.compare_right_packet(right_packet)

            if not ordered:
                packets[i], packets[i+1] = right_packet, left_packet
                swapped = True

    return packets


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        ordered_packets = []
        packet_pairs = [p for p in TEST_INPUT.split('\n\n')]
        for n, packet_pair in enumerate(packet_pairs):
            index = n+1
            left_msg, right_msg  = packet_pair.split('\n')
            left_packet = ElfPacket(left_msg, index)
            right_packet = ElfPacket(right_msg, index)
            print(index, left_packet.compare_right_packet(right_packet))

            if left_packet.compare_right_packet(right_packet):
                ordered_packets.append(left_packet)

        return sum([packet.index for packet in ordered_packets])

    @property
    def first(self):
        ordered_packets = []
        packet_pairs = [p for p in self.file_input.split('\n\n')]

        for n, packet_pair in enumerate(packet_pairs):
            index = n+1
            left_msg, right_msg  = packet_pair.split('\n')
            left_packet = ElfPacket(left_msg, index)
            right_packet = ElfPacket(right_msg, index)

            if left_packet.compare_right_packet(right_packet):
                ordered_packets.append(left_packet)

        return sum([packet.index for packet in ordered_packets])

    @property
    def test2(self):
        packet_pairs = [p for p in TEST_INPUT.split('\n\n')]

        # Divider Packets
        divider_packet_2 = ElfPacket('[[2]]')
        divider_packet_6 = ElfPacket('[[6]]')
        packets = [divider_packet_2, divider_packet_6]

        for packet_pair in packet_pairs:
            left_msg, right_msg  = packet_pair.split('\n')
            packets.append(ElfPacket(left_msg))
            packets.append(ElfPacket(right_msg))

        sorted_packets = sort_packets(packets)
        divider_2_index = sorted_packets.index(divider_packet_2) + 1
        divider_6_index = sorted_packets.index(divider_packet_6) + 1
        decoder_key = divider_2_index * divider_6_index
        return decoder_key


    @property
    def second(self):
        packet_pairs = [p for p in self.file_input.split('\n\n')]

        # Divider Packets
        divider_packet_2 = ElfPacket('[[2]]')
        divider_packet_6 = ElfPacket('[[6]]')
        packets = [divider_packet_2, divider_packet_6]

        for packet_pair in packet_pairs:
            left_msg, right_msg  = packet_pair.split('\n')
            packets.append(ElfPacket(left_msg))
            packets.append(ElfPacket(right_msg))

        sorted_packets = sort_packets(packets)
        divider_2_index = sorted_packets.index(divider_packet_2) + 1
        divider_6_index = sorted_packets.index(divider_packet_6) + 1
        decoder_key = divider_2_index * divider_6_index
        return decoder_key

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
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("test 2 solution: {}".format(solution.test2))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
