"""
Basic Questions:
- How many sessions are in the logs?
- How many sessions saw a payment fail?
- How many sessions saw a payment succeed?
- On what date(s) did the sessions occur?

Intermediate Questions:
- How many unique users were logged?
- How many users succeeded in making a payment?
- How many users failed to make a payment?
- What percentage of payments failed?
- What percentage of users failed to make a payment?

Advanced Questions:
- Which user had the most sessions?
- Do you see any interesting patterns in the data?
- Do you have any hypotheses regarding the problem?
- What do you recommend for next steps?
"""
import json
from models.session import Session
from models.user import User


class Solver:
    @staticmethod
    def solve(serialized_logs):
        return Solver(serialized_logs)

    def __init__(self, serialized_logs):
        self.serialized_logs = serialized_logs

    @property
    def logs(self):
        return json.loads(self.serialized_logs)

    @property
    def sessions(self):
        sessions = [Session.from_log(log) for log in self.logs]
        return sorted(sessions, key=lambda s: s.datetime)

    @property
    def user_sessions(self):
        users = {}
        for session in self.sessions:
            if session.uid in users:
                users[session.uid].append(session)
            else:
                users[session.uid] = [session]
        return users

    @property
    def users(self):
        users = []
        for uid, sessions in self.user_sessions.items():
            user = User(uid, sessions)
            users.append(user)
        return users

    @property
    def failed_sessions(self):
        return [s for s in self.sessions if s.failed()]

    @property
    def paid_sessions(self):
        return [s for s in self.sessions if s.paid()]

    @property
    def paid_users(self):
        return [u for u in self.users if u.paid()]

    def report(self):
        return {
            # Basic Questions
            'sessions': len(self.sessions),
            'sessions failed': len(self.failed_sessions),
            'sessions paid': len(self.paid_sessions),
            'when': (self.sessions[0].datetime, self.sessions[-1].datetime),

            # Intermediate Questions
            'unique users': len(self.users),
            'users paid': len(self.paid_users),
            'users failed': 0,
            'users failed then paid': 0,
            'payments attempted': 0,
            'payments failed': 0,
            'payment failed %': 0.0,
            'user failed %': 0.0

            # Advanced Questions
        }
