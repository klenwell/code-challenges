import random
import json
import base64
from datetime import datetime, timedelta
from functools import cached_property
from models.session import Session


class Puzzler:
    SCHEMA = [
        # method, args, count
        (Session.successful_payment, [1], 21),
        (Session.successful_payment, [2], 5),
        (Session.successful_payment, [3], 2),
        (Session.successful_payment, [6], 1),
        (Session.bad_card_success, [], 5),
        (Session.bad_card_failure, [], 2),
        (Session.bug_expired_card_failure, [], 8),
        (Session.bug_expired_card_success, [], 2),
        (Session.bug_expired_card_relogin_success, [], 1),
        (Session.bug_expired_card_relogin_failure, [], 1),
        (Session.scammer, [1, 6], 1),
        (Session.invalid, [], 2),
    ]

    @staticmethod
    def construct():
        start_after = datetime(2022, 10, 31, 1)
        duration = 6  # hours
        puzzle = Puzzler(Puzzler.SCHEMA, start_after, duration)
        return puzzle

    def __init__(self, schema, start_after, duration):
        self.schema = schema
        self.start_after = start_after
        self.duration = duration

    def report(self):
        return {
            'sessions': len(self.sessions),
            'when': (self.start_after, self.end_by),
            'len json': len(self.serialized_logs),
            'len base64': len(self.encoded_logs)
        }

    def to_file(self, fname='session_log.json'):
        self.fname = fname
        with open(self.fname, 'w') as f:
            f.write(self.serialized_logs)
        return self.fname

    @cached_property
    def serialized_logs(self):
        return json.dumps([s.to_log() for s in self.sessions])

    @property
    def encoded_logs(self):
        return str(base64.b64encode(self.serialized_logs.encode()), 'ascii')

    @cached_property
    def sessions(self):
        sessions = []
        for method, args, count in self.schema:
            for n in range(count):
                # Need to pop and replace each iternation
                args.append(self.random_ts())
                new_sessions = method(*args)
                sessions += new_sessions
                args.pop()
        return sessions

    @property
    def unix_start_after(self):
        return int(self.start_after.timestamp())

    @property
    def unix_end_by(self):
        return int(self.end_by.timestamp())

    @property
    def end_by(self):
        return self.start_after + timedelta(hours=self.duration)

    def random_ts(self):
        return random.randint(self.unix_start_after, self.unix_end_by)
