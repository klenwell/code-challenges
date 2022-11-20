import random
from datetime import datetime


class Fizzer:
    @staticmethod
    def is_mistake(log):
        ts = log[:10]
        value = log[10:]
        fizz = Fizzer(ts)
        return value != fizz.buzz()

    def __init__(self, number):
        self.number = int(number)

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.number)

    @property
    def day_of_week(self):
        return self.datetime.strftime('%A')

    def buzz(self):
        if self.is_fizzbuzz():
            return 'fizzbuzz'
        elif self.is_fizz():
            return 'fizz'
        elif self.is_buzz():
            return 'buzz'
        else:
            return ''

    def to_log(self):
        return '{}{}'.format(self.number, self.buzz())

    def is_fizz(self):
        return self.number % 3 == 0

    def is_buzz(self):
        return self.number % 5 == 0

    def is_fizzbuzz(self):
        return self.is_fizz() and self.is_buzz()


class FaultyFizzer(Fizzer):
    def __init__(self, number, error_rate):
        self.number = int(number)
        self.error_rate = error_rate

    def is_error(self):
        return random.random() < self.error_rate

    def buzz(self):
        options = ['fizz', 'buzz', 'fizzbuzz', '']
        correct_result = super().buzz()

        if not self.is_error():
            return correct_result

        wrong_results = set(options) - set([correct_result])
        return random.choice(list(wrong_results))
