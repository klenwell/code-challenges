import base64
from datetime import datetime
from models.fizzer import Fizzer


class Solver:
    @staticmethod
    def solve(encoded_logs):
        return Solver(encoded_logs)

    def __init__(self, encoded_logs):
        self.encoded_logs = encoded_logs

    @property
    def logs(self):
        delim = '\n'
        logs = (base64.b64decode(self.encoded_logs).decode()).split(delim)
        return sorted(logs)

    @property
    def start_date(self):
        ts = int(self.logs[0][:10])
        return datetime.fromtimestamp(ts)

    @property
    def end_date(self):
        ts = int(self.logs[-1][:10])
        return datetime.fromtimestamp(ts)

    @property
    def mistakes(self):
        mistakes = []
        for log in self.logs:
            if Fizzer.is_mistake(log):
                mistakes.append(log)
        return mistakes

    def value_by_day_of_week(self, value):
        counts = {}
        for log in self.logs:
            fizzer = Fizzer(log[:10])
            if fizzer.buzz() == value:
                count = counts.get(fizzer.day_of_week, 0)
                counts[fizzer.day_of_week] = count + 1
        return counts

    def mistakes_by_value(self):
        counts = {}
        for log in self.mistakes:
            fizzer = Fizzer(log[:10])
            value = fizzer.buzz()
            count = counts.get(value, 0)
            counts[value] = count + 1
        return counts

    def report(self):
        return {
            'logs': len(self.logs),
            'when': (self.start_date, self.end_date),
            'error rate': len(self.mistakes) / len(self.logs),
            'mistakes': self.mistakes,
            'fizzbuzz by day-of-week': self.value_by_day_of_week('fizzbuzz'),
            'mistakes by value': self.mistakes_by_value()
        }
