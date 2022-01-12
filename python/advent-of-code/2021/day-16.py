"""
Advent of Code 2021 - Day 16
https://adventofcode.com/2021/day/16
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import time
import math


INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')
DEBUG = 0


class Transmission:
    HEX_BIT_MAP = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }

    def __init__(self, hex_string):
        self.hex = hex_string

    @property
    def bits(self):
        bit_str = ''
        for char in list(self.hex):
            byte = self.HEX_BIT_MAP[char]
            bit_str += byte
        return bit_str

    @property
    def packet(self):
        return Packet(self.bits).by_type()

    @property
    def packets(self):
        return self.collect_packets(self.packet)

    def collect_packets(self, packet):
        packets = [packet]
        for subpacket in packet.subpackets:
            packets += self.collect_packets(subpacket)
        return packets


class Packet:
    #
    # Constructor
    #
    def __init__(self, bit_string):
        self.bits = bit_string

    #
    # Properties
    #
    @property
    def header(self):
        return self.bits[:6]

    @property
    def message(self):
        if not self.overflow:
            return self.bits
        else:
            return self.bits.rsplit(self.overflow, 1)[0]

    @property
    def version(self):
        bits = self.header[:3]
        return int(bits, 2)

    @property
    def type_id(self):
        bits = self.header[3:]
        return int(bits, 2)

    @property
    def subpackets(self):
        return []

    @property
    def subpacket_count(self):
        return len(self.subpackets)

    @property
    def version_sum(self):
        sum = 0
        for subpacket in self.subpackets:
            sum += subpacket.version_sum
        return self.version + sum

    #
    # Methods
    #
    def by_type(self):
        if self.is_value():
            return ValuePacket(self.bits)
        elif self.is_operator():
            return OperatorPacket(self.bits)
        else:
            raise ValueError('Unrecognized packet')

    def is_value(self):
        return self.type_id == 4

    def is_operator(self):
        return not self.is_value()

    def debug(self, *messages):
        if DEBUG:
            print("[LOG: {}] {}".format(time.time(), messages))

    def chunk(self, seq, size):
        """https://stackoverflow.com/a/434328/1093087"""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def __repr__(self):
        return '{}(type_id={} version={})'.format(
            self.__class__.__name__,
            self.type_id,
            self.version
        )


class ValuePacket(Packet):
    def __init__(self, bits):
        self.bits = bits
        self.debug('>', self)

    @property
    def value(self):
        bit_str = ''
        for bit_group in self.chunk(self.value_bits, 5):
            bit_str += bit_group[1:]
        return int(bit_str, 2)

    @property
    def value_bits(self):
        bit_str = ''
        for bit_group in self.chunk(self.bits[6:], 5):
            bit_str += bit_group
            if bit_group[0] == '0':
                break
        return bit_str

    @property
    def subpackets(self):
        return []

    @property
    def overflow(self):
        starts_at = len(self.header) + len(self.value_bits)
        return self.bits[starts_at:]

    def __repr__(self):
        return '{}(version={} value={} msglen={} bitlen={})'.format(
            self.__class__.__name__,
            self.version,
            self.value,
            len(self.message),
            len(self.bits)
        )


class OperatorPacket(Packet):
    def __init__(self, bits):
        self.bits = bits
        self.debug('>', self)

    #
    # Properties
    #
    @property
    def value(self):
        sub_values = [sub.value for sub in self.subpackets]

        if self.type_id == 0:
            return sum(sub_values)
        elif self.type_id == 1:
            return math.prod(sub_values)
        elif self.type_id == 2:
            return min(sub_values)
        elif self.type_id == 3:
            return max(sub_values)
        elif self.type_id == 4:
            pass
        elif self.type_id == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type_id == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type_id == 7:
            return 1 if sub_values[0] == sub_values[1] else 0

    @property
    def length_type_id(self):
        return int(self.bits[6])

    @property
    def length_type(self):
        if self.length_based_subpackets():
            return 'length-based'
        else:
            return 'count-based'

    @property
    def length_bits(self):
        if self.length_based_subpackets():
            return self.bits[7:22]
        else:
            return self.bits[7:18]

    @cached_property
    def subpackets(self):
        if self.length_based_subpackets():
            return self.parse_subpacket_bits(self.subpacket_bits)
        elif self.count_based_subpackets():
            return self.parse_subpacket_bits(self.subpacket_bits, max_packets=self.subpacket_count)
        raise ValueError('Unexpected operator subpacket mode.')

    @property
    def subpacket_length(self):
        if self.length_based_subpackets():
            return int(self.length_bits, 2)
        else:
            raise TypeError('Subpackets not marked by length.')

    @property
    def subpacket_count(self):
        if self.count_based_subpackets():
            subpacket_count_bits = self.bits[7:18]
            return int(subpacket_count_bits, 2)
        else:
            return len(self.subpackets)

    @property
    def subpacket_bits(self):
        starts_at = len(self.header) + 1 + len(self.length_bits)

        if self.length_based_subpackets():
            ends_at = starts_at + self.subpacket_length
            return self.bits[starts_at:ends_at]
        elif self.count_based_subpackets():
            return self.bits[starts_at:]

    @property
    def overflow(self):
        """overflow is extra bits at the end of some packets. This is a pretty crappy
        protocol when you think about it. It really needs a terminal bit marker.
        """
        if self.length_based_subpackets():
            starts_at = len(self.header) + 1 + len(self.length_bits) + self.subpacket_length
        elif self.count_based_subpackets():
            subpackets_len = sum([len(sub.message) for sub in self.subpackets])
            starts_at = len(self.header) + 1 + len(self.length_bits) + subpackets_len
        else:
            raise TypeError('Overflow issue!')

        return self.bits[starts_at:]

    #
    # Methods
    #
    def parse_subpacket_bits(self, subpacket_bits, max_packets=None):
        subpacket = Packet(subpacket_bits).by_type()
        subpackets = [subpacket]

        while subpacket.overflow:
            if max_packets and len(subpackets) == max_packets:
                return subpackets

            subpacket = Packet(subpacket.overflow).by_type()
            subpackets.append(subpacket)

        return subpackets

    def length_based_subpackets(self):
        return self.length_type_id == 0

    def count_based_subpackets(self):
        return self.length_type_id == 1

    def dump(self):
        return (
            ('version', self.version),
            ('type_id', self.type_id),
            ('header', self.header),
            ('length_type_id', self.length_type_id),
            ('length_bits', self.length_bits),
            ('subpacket_bits', self.subpacket_bits),
            ('overflow', self.overflow),
            ('bits', self.bits)
        )

    def __repr__(self):
        return '{}(version={} type={}:{} bitlen={})'.format(
            self.__class__.__name__,
            self.version,
            self.length_type_id,
            self.length_type,
            len(self.bits)
        )


class Solution:
    #
    # Tests
    #
    @staticmethod
    def test_1():
        hex_string = 'D2FE28'
        transmission = Transmission(hex_string)
        packet = transmission.packet

        assert packet.is_value()
        assert packet.bits == '110100101111111000101000'
        assert packet.version == 6, packet.version
        assert packet.type_id == 4
        assert packet.value == 2021, packet.literal_value
        return 'PASS'

    @staticmethod
    def test_2():
        hex_string = '38006F45291200'
        transmission = Transmission(hex_string)
        packet = transmission.packet

        assert packet.is_operator()
        assert packet.length_based_subpackets()
        assert [p.value for p in packet.subpackets] == [10, 20]
        return 'PASS'

    @staticmethod
    def test_3():
        hex_string = 'EE00D40C823060'
        transmission = Transmission(hex_string)
        packet = transmission.packet

        assert packet.is_operator()
        assert packet.count_based_subpackets()
        assert [p.value for p in packet.subpackets] == [1, 2, 3]
        return 'PASS'

    @staticmethod
    def test_4():
        cases = [
            # hex_string, expected_sum
            ('8A004A801A8002F478', 16),
            ('620080001611562C8802118E34', 12),
            ('C0015000016115A2E0802F182340', 23),
            ('A0016C880162017C3686B18A3D4780', 31)
        ]

        for hex_string, expected_sum in cases:
            transmission = Transmission(hex_string)
            packet = transmission.packet
            assert packet.version_sum == expected_sum, (hex_string, packet.version_sum)

        return 'PASS'

    #
    # Solutions
    #
    @staticmethod
    def first():
        solution = Solution(INPUT_FILE)
        hex_string = solution.input_lines[0]
        transmission = Transmission(hex_string)
        packet = transmission.packet
        return packet.version_sum

    @staticmethod
    def second():
        solution = Solution(INPUT_FILE)
        hex_string = solution.input_lines[0]
        transmission = Transmission(hex_string)
        packet = transmission.packet
        return packet.value

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #
    def __init__(self, input_file):
        self.input_file = input_file


#
# Main
#
print("test 1: {}".format(Solution.test_1()))
print("test 2: {}".format(Solution.test_2()))
print("test 3: {}".format(Solution.test_3()))
print("test 4: {}".format(Solution.test_4()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
