"""
New-line separated string, base64-encoded, of about 100 lines. Format:

- unix-timestamp
- fizzbuzz computation: <blank> | 'fizz' | 'buzz' | 'fizzbuzz'
- Computation is based on timestamp

Examples:
- `1668817445fizzbuzz`
- `1668817504`
- Encoded: `MTY2ODgxNzQ0NWZpenpidXp6CjE2Njg4MTc1MDQ=`

Questions:

- How many records are there?
- When were the records generated?
- What day of the week had the most 'fizzbuzz' computations?
- How many records had an incorrect computation?
- Which computation was miscalculated most frequently?

"""
import base64
from datetime import datetime, timedelta
from random import randint
from models.fizzer import FaultyFizzer


class Puzzler:
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

    @property
    def start_ts(self):
        return int(self.start_date.timestamp())

    @property
    def end_ts(self):
        return int((self.start_date + timedelta(days=self.days)).timestamp())

    @property
    def logs(self):
        logs = []
        for n in range(self.count):
            timestamp = randint(self.start_ts, self.end_ts)
            fizzer = FaultyFizzer(timestamp, .08)
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

    def report(self):
        return {
            'encoded_logs': self.encoded_logs,
            'len(serialized_logs)': len(self.serialized_logs),
            'len(encoded_logs)': len(self.encoded_logs),
            'logs': self.logs
        }
