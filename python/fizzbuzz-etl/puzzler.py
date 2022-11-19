import base64
from datetime import datetime, timedelta
from random import randint
from functools import cached_property
from models.fizzer import FaultyFizzer


class Puzzler:
    ERROR_RATE = 0.10

    @staticmethod
    def construct():
        count = 122
        start_date = datetime(2023, 1, 1)
        puzzle = Puzzler(count, start_date)
        return puzzle

    def __init__(self, count, start_date, days=7):
        self.count = count
        self.start_date = start_date
        self.days = days
        self.fname = None

    @property
    def start_ts(self):
        return int(self.start_date.timestamp())

    @property
    def end_ts(self):
        return int((self.start_date + timedelta(days=self.days)).timestamp())

    @cached_property
    def logs(self):
        logs = []
        for n in range(self.count):
            timestamp = randint(self.start_ts, self.end_ts)
            fizzer = FaultyFizzer(timestamp, self.ERROR_RATE)
            logs.append(fizzer.to_log())
        return logs

    @property
    def serialized_logs(self):
        delim = '\n'
        return delim.join(self.logs)

    @property
    def encoded_logs(self):
        return str(base64.b64encode(self.serialized_logs.encode()), 'ascii')

    def decoded_logs(self, encoded_logs):
        delim = '\n'
        return (base64.b64decode(encoded_logs).decode()).split(delim)

    def to_file(self, fname='encoded_log.txt'):
        self.fname = fname
        with open(self.fname, 'w') as f:
            f.write(self.encoded_logs)
        return self.fname

    def report(self):
        return {
            'encoded_logs': self.encoded_logs,
            'len(serialized_logs)': len(self.serialized_logs),
            'len(encoded_logs)': len(self.encoded_logs),
            'logs': self.logs,
            'file': self.fname
        }
