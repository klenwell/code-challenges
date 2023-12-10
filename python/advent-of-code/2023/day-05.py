"""
Advent of Code 2023 - Day 5
https://adventofcode.com/2023/day/5

It took me a while to solve this. To finally do so, I imagined each range of seeds grouped
together as a long pod (hence the SeedPod class) with all the pods lined up at the edge of
a field. I imagined the category mappings as a series of gates across the field which every
seed needed to navigate. To do so, the pod would send out its lead (seed with lowest id in pod)
which would run to the next gate and figure out how many seeds in its pod could go through
that gate.

The first seed not handled by that mapping gate would be told to take the rest of the seeds in
the pod and create a new pod where it would be lead seed. The lead seed of the new pod would
then look for the mapping gate it was supposed to pass through. This would go on recursively
until all pods had passed through a gate. They would continue from gate to gate until they all
passed through the last mapping gate.

Then it was just a matter of sorting the pods by the location value of their lead seeds.
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class SeedAlmanac:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def lowest_location(self):
        sorted_seeds = sorted(self.seeds, key=lambda s: s.location)
        return sorted_seeds[0].location

    @cached_property
    def seeds(self):
        seeds = []
        seed_block = self.blocks[0]
        _, ids = seed_block.split(':')
        for id in ids.strip().split(' '):
            seed = Seed(int(id), self)
            seeds.append(seed)
        return seeds

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
    def mapping_pages(self):
        return self.pages[1:]

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


class Seed:
    def __init__(self, id, almanac):
        self.id = id
        self.almanac = almanac

    @cached_property
    def seed(self):
        # Alias for id required because almanac refers uses "seed" to id
        return self.id

    @cached_property
    def location(self):
        return self.almanac.map_value_from_category('humidity', self.humidity)

    @cached_property
    def humidity(self):
        return self.almanac.map_value_from_category('temperature', self.temperature)

    @cached_property
    def temperature(self):
        return self.almanac.map_value_from_category('light', self.light)

    @cached_property
    def light(self):
        return self.almanac.map_value_from_category('water', self.water)

    @cached_property
    def water(self):
        return self.almanac.map_value_from_category('fertilizer', self.fertilizer)

    @cached_property
    def fertilizer(self):
        return self.almanac.map_value_from_category('soil', self.soil)

    @cached_property
    def soil(self):
        return self.almanac.map_value_from_category('seed', self.id)


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
        if 'map' not in self.header:
            return None
        _, right = self.header.split('-to-')
        maps_to, _ = right.split(' ')
        return maps_to.strip()

    @property
    def maps_from(self):
        if 'map' not in self.header:
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

    def find_mapping_for_seed(self, seed):
        for mapping in self.mappings:
            if mapping.includes_seed(seed):
                return mapping
        return None

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
        return self.min_in + self.length - 1

    @property
    def min_out(self):
        min_out, _, _ = self.line.split()
        return int(min_out)

    @property
    def length(self):
        _, _, length = self.line.split()
        return int(length)

    @cached_property
    def category(self):
        return self.page.maps_from

    def map_from_value(self, value):
        if not self.includes_value(value):
            raise Exception(f"{self} does not map {value}")
        offset = value - self.min_in
        return self.min_out + offset

    def includes_seed(self, seed):
        value = getattr(seed, self.category)
        return self.includes_value(value)

    def includes_value(self, value):
        return self.min_in <= value <= self.max_in

    def encompasses_pod(self, pod):
        return self.max_in >= pod.max_value_for_category(self.category)

    def how_many_seeds_from_pod(self, pod):
        lead_seed_value_in = getattr(pod.lead_seed, self.category)
        offset = lead_seed_value_in - self.min_in
        return self.length - offset

    def __repr__(self):
        maps = f"{self.min_in}->{self.min_out}"
        return f"<Mapping page={self.page.number} {maps} length={self.length}>"


class PodAlmanac(SeedAlmanac):
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def pods(self):
        seed_block = self.blocks[0]
        return SeedPod.extract_from_ranges(seed_block, self)

    @cached_property
    def lowest_location(self):
        pods = list(self.pods)

        for page in self.mapping_pages:
            pods_out = []
            for pod in pods:
                pods = self.map_pod_by_page(pod, page)
                pods_out += pods
            pods = list(pods_out)

        sorted_pods = sorted(pods, key=lambda p: p.lead_seed.location)
        print(len(sorted_pods), sorted_pods[0])
        return sorted_pods[0].lead_seed.location

    def map_pod_by_page(self, pod, page):
        # Send lead seed in pod to next gate
        seed = pod.lead_seed

        # Find mapping
        mapping = page.find_mapping_for_seed(pod.lead_seed)

        # If no mapping, create a NullMapping mapping
        if not mapping:
            mapping = NullMapping(pod, page)

        # If pod fits in mapping, done!
        if mapping.encompasses_pod(pod):
            return [pod]

        # Pod too big for mapping? Split pod to fit
        seeds_mapped = mapping.how_many_seeds_from_pod(pod)
        new_pod_lead_id = seed.id + seeds_mapped
        new_pod = pod.split_at_id(new_pod_lead_id)
        # breakpoint()

        return [pod] + self.map_pod_by_page(new_pod, page)


class SeedPod:
    @staticmethod
    def extract_from_ranges(input, almanac):
        pods = []
        _, ids = input.split(':')
        seed_ids = ids.strip().split()

        for n in range(len(seed_ids)):
            if n % 2 == 0:
                continue
            start_id = int(seed_ids[n-1])
            length = int(seed_ids[n])
            pod = SeedPod(start_id, length, almanac)
            pods.append(pod)

        print(pods)
        return pods

    def __init__(self, lead_id, length, almanac):
        self.lead_id = lead_id
        self.length = length
        self.almanac = almanac

    @cached_property
    def lead_seed(self):
        return Seed(self.lead_id, self.almanac)

    @cached_property
    def min_location(self):
        return self.lead_seed.location

    def max_value_for_category(self, category):
        lead_seed_category_value = getattr(self.lead_seed, category)
        return lead_seed_category_value + self.length

    def split_at_id(self, seed_id):
        old_pod_length = seed_id - self.lead_seed.id
        new_pod_length = self.length - old_pod_length
        new_pod = SeedPod(seed_id, new_pod_length, self.almanac)
        self.length = old_pod_length
        return new_pod

    def __repr__(self):
        return f"<Pod lead_id={self.lead_id} length={self.length}>"


class NullMapping(Mapping):
    def __init__(self, pod, page):
        pod_category_value = getattr(pod.lead_seed, page.maps_from)
        next_page_mapping = self.find_next_mapping_for_page(page, pod_category_value)
        length = next_page_mapping.min_in - pod_category_value if next_page_mapping else 1000000000
        line = f"{pod_category_value} {pod_category_value} {length}"
        super().__init__(line, page)

    def find_next_mapping_for_page(self, page, value):
        sorted_mappings = sorted(page.mappings, key=lambda m: m.min_in)
        for n, mapping in enumerate(sorted_mappings):
            last_max_in = sorted_mappings[n-1].max_in if n > 1 else 0
            next_min_in = mapping.min_in
            if last_max_in < value < next_min_in:
                return mapping
        return None


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
        almanac = SeedAlmanac(input)
        result = almanac.lowest_location
        assert result == 265018614, result
        return result

    @property
    def second(self):
        input = self.file_input
        almanac = PodAlmanac(input)
        assert almanac.lowest_location == 63179500, almanac.lowest_location
        return almanac.lowest_location

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        almanac = SeedAlmanac(input)
        result = almanac.lowest_location
        assert result == 35, result
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        almanac = PodAlmanac(input)

        page = almanac.pages[1]
        pod = almanac.pods[0]

        assert page.maps_from == 'seed', page
        assert page.maps_to == 'soil', page
        assert pod.lead_id == 79, pod

        result = almanac.lowest_location
        assert result == 46, result
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
