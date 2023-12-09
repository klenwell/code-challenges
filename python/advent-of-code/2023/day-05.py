"""
Advent of Code 2023 - Day 5
https://adventofcode.com/2023/day/5
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class Almanac:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def blocks(self):
        return [block.strip() for block in self.input.split("\n\n")]

    @cached_property
    def pages(self):
        pages = []
        for n in range(len(self.blocks)):
            page = Page(n, self)
            pages.append(page)
        return pages

    @cached_property
    def seeds(self):
        seeds = []
        seed_block = self.blocks[0]
        _, ids = seed_block.split(':')
        for id in ids.strip().split(' '):
            seed = Seed(int(id), self)
            seeds.append(seed)
        return seeds

    def map_value_from_category(self, category, value):
        page = self.find_page_by_category(category)
        for mapping in page.mappings:
            if mapping.includes_value(value):
                return mapping.map_from_value(value)
        # If mapping not found, return original value
        return value

    def find_page_by_category(self, category):
        for page in self.pages:
            if page.maps_from == category:
                return page
        raise Exception(f"page for {category} not found")

    def find_lowest_location_number(self):
        sorted_seeds = sorted(self.seeds, key=lambda s: s.location)
        return sorted_seeds[0].location

    def map_humidity_to_location(self, value):
        block_index = 7
        return self.map_value_by_block(value, block_index)

    def map_temperature_to_humidity(self, value):
        block_index = 6
        return self.map_value_by_block(value, block_index)

    def map_light_to_temperature(self, value):
        block_index = 5
        return self.map_value_by_block(value, block_index)

    def map_water_to_light(self, value):
        block_index = 4
        return self.map_value_by_block(value, block_index)

    def map_fertilizer_to_water(self, value):
        block_index = 3
        return self.map_value_by_block(value, block_index)

    def map_soil_to_fertilizer(self, value):
        block_index = 2
        return self.map_value_by_block(value, block_index)

    def map_seed_to_soil(self, value):
        block_index = 1
        return self.map_value_by_block(value, block_index)

    def map_value_by_block(self, value, block_index):
        block = self.blocks[block_index]
        lines = block.split("\n")

        for line in lines[1:]:
            min_dest, min_source, range = line.strip().split()
            min_source = int(min_source)

            max_source = min_source + int(range)
            if min_source <= value < max_source:
                offset = value - min_source
                mapped_value = int(min_dest) + offset
                return mapped_value

        return value

    def build_range_map_naively(self, block_index):
        # LOL: Does not work with huge ranges
        mapping = {}
        block = self.blocks[block_index]
        lines = block.split("\n")

        for line in lines[1:]:
            dest, source, length = line.strip().split()
            for n in range(int(length)):
                key = int(source) + n
                val = int(dest) + n
                mapping[key] = val

        return mapping


class Seed:
    def __init__(self, id, almanac):
        self.id = id
        self.almanac = almanac

    @cached_property
    def location(self):
        return self.almanac.map_humidity_to_location(self.humidity)

    @cached_property
    def humidity(self):
        return self.almanac.map_temperature_to_humidity(self.temperature)

    @cached_property
    def temperature(self):
        return self.almanac.map_light_to_temperature(self.light)

    @cached_property
    def light(self):
        return self.almanac.map_water_to_light(self.water)

    @cached_property
    def water(self):
        return self.almanac.map_fertilizer_to_water(self.fertilizer)

    @cached_property
    def fertilizer(self):
        return self.almanac.map_soil_to_fertilizer(self.soil)

    @cached_property
    def soil(self):
        return self.almanac.map_seed_to_soil(self.id)


class PodAlmanac(Almanac):
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def pods(self):
        seed_block = self.blocks[0]
        return SeedPod.extract_from_ranges(seed_block)

    def find_lowest_location_number_backwards(self):
        location_page = self.pages[7]
        min_location_mapping = sorted(location_page.mappings, key=lambda p: p.min_dest)[0]
        print(min_location_mapping)
        seed_packet = SeedPacket(min_location_mapping)
        init_packet = seed_packet.source_seeds()
        return init_packet


class SeedPod:
    @staticmethod
    def extract_from_ranges(input):
        pods = []
        _, ids = input.split(':')
        seed_ids = ids.strip().split()

        for n in range(len(seed_ids)):
            if n % 2 == 0:
                continue
            start_id = int(seed_ids[n-1])
            length = int(seed_ids[n])
            pod = SeedPod(start_id, length, self)
            pods.append(pod)

        return pods

    def __init__(self, start_id, length, almanac):
        self.start_id = start_id
        self.end_id = start_id + length - 1
        self.length = length
        self.almanac = almanac

    def __repr__(self):
        return f"<Pod start_id={self.start_id} length={self.length}>"


class Page:
    def __init__(self, number, almanac):
        self.almanac = almanac
        self.number = number

    @property
    def content(self):
        return self.almanac.blocks[self.number].strip()

    @property
    def lines(self):
        return self.content.split('\n')

    @property
    def header(self):
        return self.lines[0]

    @property
    def maps_to(self):
        if not 'map' in self.header:
            return None
        _, right = self.header.split('-to-')
        maps_to, _ = right.split(' ')
        return maps_to.strip()

    @property
    def maps_from(self):
        if not 'map' in self.header:
            return None
        maps_from, _ = self.header.split('-to-')
        return maps_from.strip()

    @property
    def mappings(self):
        mappings = []
        for line in self.lines[1:]:
            mapping = Mapping(line, self)
            mappings.append(mapping)
        return mappings

    def __repr__(self):
        maps = f"{self.maps_from}->{self.maps_to}"
        return f"<Page number={self.number} {maps}>"


class Mapping:
    def __init__(self, line, page):
        self.line = line.strip()
        self.page = page

    @property
    def min_in(self):
        _, min_in, _ = self.line.split()
        return int(min_in)

    @property
    def max_in(self):
        return self.min_in + self.length

    @property
    def min_out(self):
        min_out, _, _ = self.line.split()
        return int(min_out)

    @property
    def length(self):
        _, _, length = self.line.split()
        return int(length)

    def map(self, value):
        if value < self.min_in or value > self.max_in:
            raise Exception(f"{self} does not map {value}")


    def map_from_value(self, value):
        if not self.includes_value(value):
            raise Exception(f"{self} does not map {value}")
        offset = value - self.min_in
        return self.min_out + offset

    def includes_value(self, value):
        return self.min_in <= value <= self.max_in

    def __repr__(self):
        maps = f"{self.min_in}->{self.min_out}"
        return f"<Mapping page={self.page.number} {maps} length={self.length}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-05.txt')

    TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

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
        almanac = Almanac(input)
        lowest_loc_number = almanac.find_lowest_location_number()
        return lowest_loc_number

    @property
    def second(self):
        input = self.file_input
        almanac = ExtendedAlmanac(input)

        location_entry = almanac.find_lowest_location_entry()
        print(location_entry)

        entries = almanac.find_parent_entries(location_entry)
        entries = almanac.find_parent_entries(entries[0])
        entries = almanac.find_parent_entries(entries[0])
        entries = almanac.find_parent_entries(entries[0])
        entries = almanac.find_parent_entries(entries[0])
        entries = almanac.find_parent_entries(entries[0])
        print(entries)

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        almanac = Almanac(input)
        lowest_loc_number = almanac.find_lowest_location_number()
        assert lowest_loc_number == 35, lowest_loc_number
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        almanac = PodAlmanac(input)

        page = almanac.pages[1]
        pod = almanac.pods[0]

        assert page.maps_from == 'seed', page
        assert page.maps_to == 'soil', page
        assert pod.start_id == 79, pod
        assert pod.end_id == 92, pod

        lowest_loc_number = almanac.lowest_location
        assert lowest_loc_number == 46, lowest_loc_number
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
