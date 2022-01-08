"""
Advent of Code 2021 - Day 16
https://adventofcode.com/2021/day/16
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')


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
    def version(self):
        bits = self.header[:3]
        return int(bits, 2)

    @property
    def type_id(self):
        bits = self.header[3:]
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

    @property
    def overflow(self):
        if self.is_value():
            starts_at = len(self.header) + len(self.value_bits)
        else:
            starts_at = len(self.header) + sum([len(sub.bits) for sub in self.subpackets])

        return self.bits[starts_at:]

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

    def parse_subpacket_bits(self, subpacket_bits, max_packets=None):
        print('subpacket {} from {} {}'.format(subpacket_bits, self, self.bits))

        packet = Packet(subpacket_bits).by_type()
        packets = [packet]

        while packet.overflow:
            packet = Packet(packet.overflow).by_type()
            packets.append(packet)

            if max_packets and len(packets) >= max_packets:
                break

            if not self.valid_subpacket_bits(packet.overflow):
                f = "Invalid subpacket bits: {} left of {}"
                print(f.format(packet.overflow, subpacket_bits))
                return packets

        return packets

    def valid_subpacket_bits(self, bit_str):
        if len(bit_str) < 6:
            return False

        return True

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
        print(self)

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

    def __repr__(self):
        return '{}(version={} value={})'.format(
            self.__class__.__name__,
            self.version,
            self.value
        )


class OperatorPacket(Packet):
    def __init__(self, bits):
        self.bits = bits
        print(self)

    @property
    def length_type_id(self):
        return int(self.bits[6])

    @property
    def length_bits(self):
        if self.length_based_subpackets():
            return self.bits[7:22]
        else:
            raise ValueError('Subpackets not marked by length.')

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
            raise ValueError('Subpackets not marked by length.')

    @property
    def subpacket_count(self):
        if self.count_based_subpackets():
            subpacket_count_bits = self.bits[7:18]
            return int(subpacket_count_bits, 2)
        else:
            return len(self.subpackets)

    @property
    def subpacket_bits(self):
        if self.length_based_subpackets():
            start_at = len(self.header) + 1 + len(self.length_bits)
            end_at = start_at + self.subpacket_length
            return self.bits[start_at:end_at]
        elif self.count_based_subpackets():
            start_at = len(self.header) + 1 + 11
            return self.bits[start_at:]

    def length_based_subpackets(self):
        return self.length_type_id == 0

    def count_based_subpackets(self):
        return self.length_type_id == 1


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
        assert packet.bits == '00111000000000000110111101000101001010010001001000000000'
        assert packet.version == 1, packet.version
        assert packet.type_id == 6
        assert packet.length_type_id == 0
        assert packet.length_bits == '000000000011011', packet.length_bits
        assert packet.subpacket_length == 27
        assert len(packet.subpackets) == 2, len(packet.subpackets)
        assert [p.value for p in packet.subpackets] == [10, 20]
        return 'PASS'

    @staticmethod
    def test_3():
        hex_string = 'EE00D40C823060'
        transmission = Transmission(hex_string)
        packet = transmission.packet

        assert packet.is_operator()
        assert packet.version == 7, packet.version
        assert packet.type_id == 3
        assert packet.length_type_id == 1
        assert(packet.subpacket_bits == '01010000001100100000100011000001100000',
               packet.subpacket_bits)
        assert packet.subpacket_count == 3
        assert len(packet.subpackets) == 3, len(packet.subpackets)
        assert [p.value for p in packet.subpackets] == [1, 2, 3]
        return 'PASS'

    @staticmethod
    def test_4():
        hex_string = '8A004A801A8002F478'
        expected_sum = 16
        transmission = Transmission(hex_string)
        packet = transmission.packet

        print(packet.bits)

        assert packet.is_operator()
        assert packet.version_sum == expected_sum, (packet.version_sum, expected_sum)
        return 'PASS'

    @staticmethod
    def test_5():
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
            assert packet.version_sum == expected_sum, (hex_string, packet.version_sum, expected_sum)
            print("PASS: {}".format(hex_string))

        return 'PASS'

    #
    # Solutions
    #
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
print("test 1: {}".format(Solution.test_1()))
print("test 2: {}".format(Solution.test_2()))
print("test 3: {}".format(Solution.test_3()))
print("test 4: {}".format(Solution.test_4()))
print("value packet test: {}".format(Solution.test_value_packet()))
print("operator packet test 1: {}".format(Solution.test_operator_packet()))
print("operator packet test 2: {}".format(Solution.test_operator_packet_2()))
print("test version sums: {}".format(Solution.test_version_sums()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
