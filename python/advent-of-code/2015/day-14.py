"""
Advent of Code 2015 - Day 14
https://adventofcode.com/2015/day/14

Day 14: Reindeer Olympics
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class ReindeerOlympics:
    def __init__(self, reports):
        self.reports = reports.strip()
        self.reindeers = self.scout_reindeers(self.reports)
        self.racers = self.scout_racers(self.reports)

    def scout_reindeers(self, reports):
        reindeers = []
        for report in reports.split('\n'):
            reindeer = Reindeer(report)
            reindeers.append(reindeer)
        return reindeers

    def scout_racers(self, reports):
        racers = []
        for report in reports.split('\n'):
            racer = RacingReindeer(report)
            racers.append(racer)
        return racers

    def timed_race(self, seconds):
        racers = []
        for reindeer in self.reindeers:
            kms = reindeer.fly_far(seconds)
            racers.append((reindeer, kms))
        ordered = sorted(racers, key=lambda t: t[1], reverse=True)
        info(ordered)
        winner, kms = ordered[0]
        return (winner.name, kms)

    def scored_race(self, seconds):
        scores = {}
        for racer in self.racers:
            scores[racer] = 0

        for n in range(seconds):
            for racer in self.racers:
                racer.fly_for_second()

            ordered = sorted(self.racers, key=lambda r: r.kms, reverse=True)
            lead_km = ordered[0].kms

            scorers = [r for r in self.racers if r.kms == lead_km]

            for scorer in scorers:
                scores[scorer] += 1

            info(ordered, 250)

        ordered = sorted(scores.items(), key=lambda t: t[1], reverse=True)
        info(ordered)
        winner, score = ordered[0]
        return (winner, score)


class Reindeer:
    def __init__(self, report):
        self.report = report

    @cached_property
    def name(self):
        name, _ = self.report.split(' can')
        return name

    @cached_property
    def rate(self):
        head, _ = self.report.split(' km/s')
        _, rate = head.split('fly ')
        return int(rate)

    @cached_property
    def duration(self):
        head, _ = self.report.split(' seconds, but')
        _, duration = head.split('for ')
        return int(duration)

    @cached_property
    def rest_period(self):
        head, _ = self.report.split(' seconds.')
        _, period = head.split('rest for ')
        return int(period)

    def fly_far(self, seconds):
        distance = 0
        time = seconds
        flying = True

        while time > 0:
            if flying:
                flying = False
                if time > self.duration:
                    distance += self.rate * self.duration
                    time -= self.duration
                else:
                    distance += self.rate * time
                    time = 0
            else:  # resting
                flying = True
                time -= self.rest_period

        return distance

    def __repr__(self):
        name = self.name
        rate = self.rate
        dur = self.duration
        rest = self.rest_period
        return f"<{name} rate={rate} km/s for {dur}s rest={rest}s"


class RacingReindeer(Reindeer):
    def __init__(self, report):
        super().__init__(report)
        self.seconds = 0
        self.kms = 0

    @property
    def flying(self):
        cycle = self.duration + self.rest_period
        cycle_s = self.seconds % cycle
        fly_range = (1, self.duration+1)
        return cycle_s in range(*fly_range)

    def fly_for_second(self):
        self.seconds += 1
        if self.flying:
            self.kms += self.rate
        return self


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-14.txt')

    TEST_INPUT = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""

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
        olympics = ReindeerOlympics(input)
        (winner, distance) = olympics.timed_race(2503)
        return distance

    @property
    def second(self):
        input = self.file_input
        olympics = ReindeerOlympics(input)
        (winner, score) = olympics.scored_race(2503)
        return score

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        olympics = ReindeerOlympics(input)
        comet = olympics.reindeers[0]
        dancer = olympics.reindeers[1]

        assert comet.name == 'Comet'
        assert comet.fly_far(1000) == 1120, comet.fly_far(1000)
        assert dancer.name == 'Dancer'
        assert dancer.fly_far(1000) == 1056, dancer.fly_far(1000)

        (winner, distance) = olympics.timed_race(1000)
        assert winner == 'Comet', winner
        assert distance == 1120, distance

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        olympics = ReindeerOlympics(input)
        (winner, score) = olympics.scored_race(1000)

        assert winner.name == 'Dancer', winner
        assert score == 689, score

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
