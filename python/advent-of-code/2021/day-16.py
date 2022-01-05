"""
Advent of Code 2021 - Day 16
https://adventofcode.com/2021/day/16
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')


class Packet:
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

    @staticmethod
    def from_hex(hex_string):
        bit_string = Packet.hex_to_bits(hex_string)
        return Packet(bit_string)

    @staticmethod
    def from_subpacket_bits(bit_string):
        packet = Packet(bit_string)
        packets = [packet]

        while packet.surplus:
            packet = Packet(packet.surplus)
            packets.append(packet)

        return packets

    @staticmethod
    def hex_to_bits(hex_string):
        bit_str = ''
        for char in list(hex_string):
            byte = Packet.HEX_BIT_MAP[char]
            bit_str += byte
        return bit_str

    def __init__(self, bits):
        self.bits = bits

    @property
    def header(self):
        return self.bits[:6]

    @property
    def body(self):
        if self.type_id == 4:
            return self.bits[6:]

    @property
    def version(self):
        bits = self.header[:3]
        return int(bits, 2)

    @property
    def type_id(self):
        bits = self.header[3:]
        return int(bits, 2)

    @property
    def length_type_id(self):
        if self.type_id == 4:
            raise ValueError('Not operator packet.')
        return int(self.bits[6])

    @property
    def length_bits(self):
        return self.bits[7:22]

    @property
    def subpacket_length(self):
        return int(self.length_bits, 2)

    @property
    def subpacket_bits(self):
        start_at = len(self.header) + 1 + len(self.length_bits)
        end_at = start_at + self.subpacket_length
        return self.bits[start_at:end_at]

    @property
    def subpackets(self):
        return Packet.from_subpacket_bits(self.subpacket_bits)

    @property
    def value_bits(self):
        if self.type_id != 4:
            raise ValueError('Not literal value packet.')

        bit_str = ''

        for bit_group in self.chunk(self.body, 5):
            bit_str += bit_group
            if bit_group[0] == '0':
                break

        return bit_str

    @property
    def surplus(self):
        starts_at = len(self.header) + len(self.value_bits)
        return self.bits[starts_at:]

    @property
    def literal_value(self):
        if self.type_id != 4:
            raise ValueError('Not literal value packet.')

        bit_str = ''
        for bit_group in self.chunk(self.value_bits, 5):
            bit_str += bit_group[1:]

        return int(bit_str, 2)

    def chunk(self, seq, size):
        """https://stackoverflow.com/a/434328/1093087"""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class Solution:
    #
    # Solutions
    #
    @staticmethod
    def test():
        # Literal Value Packet
        hex_string = 'D2FE28'
        packet = Packet.from_hex(hex_string)
        assert packet.bits == '110100101111111000101000'
        assert packet.version == 6, packet.version
        assert packet.type_id == 4
        assert packet.value_bits == '101111111000101', packet.value_bits
        assert packet.literal_value == 2021, packet.literal_value

        # Operator Packet
        hex_string = '38006F45291200'
        packet = Packet.from_hex(hex_string)
        assert packet.bits == '00111000000000000110111101000101001010010001001000000000'
        assert packet.version == 1, packet.version
        assert packet.type_id == 6
        assert packet.length_type_id == 0
        assert packet.length_bits == '000000000011011', packet.length_bits
        assert packet.subpacket_length == 27
        assert len(packet.subpackets) == 2, len(packet.subpackets)
        assert [p.literal_value for p in packet.subpackets] == [10, 20]

        return 'PASS'

    @staticmethod
    def first():
        pass

    @staticmethod
    def second():
        pass

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
print("test: {}".format(Solution.test()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
