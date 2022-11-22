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
        return sorted(sessions, key=lambda s: s.created_at)

    @property
    def user_sessions(self):
        users = {}
        for session in self.sessions:
            if session.user_id in users:
                users[session.user_id].append(session)
            else:
                users[session.user_id] = [session]
        return users

    @property
    def users(self):
        users = []
        for user_id, sessions in self.user_sessions.items():
            user = User(user_id, sessions)
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

    @property
    def failed_users(self):
        return [u for u in self.users if u.failed()]

    @property
    def failed_paid_users(self):
        return [u for u in self.users if u.failed_then_paid()]

    @property
    def payments_attempted(self):
        return sum([s.payments_attempted for s in self.sessions])

    @property
    def payments_succeeed(self):
        return sum([s.payments_succeeed for s in self.sessions])

    @property
    def payments_failed(self):
        return sum([s.payments_failed for s in self.sessions])

    @property
    def users_failed_pct(self):
        failed_user_count = len(self.failed_users)
        failed_paid_user_count = len(self.failed_paid_users)
        return (failed_user_count - failed_paid_user_count) / len(self.users) * 100

    @property
    def user_with_most_sessions(self):
        return sorted(self.users, key=lambda u: len(u.sessions))[-1]

    @property
    def invalid_sessions(self):
        return [session for session in self.sessions if not session.is_valid()]

    @property
    def failure_types(self):
        types = {}
        for session in self.sessions:
            if not '*' in session.action_stream:
                continue
            for i, char in enumerate(session.action_stream):
                if char == '*':
                    before = session.action_stream[i-1]
                    after = session.action_stream[i+1]
                    if (before, after) in types:
                        types[(before, after)].append(session)
                    else:
                        types[(before, after)] = [session]
        return types

    def recoveries_by_seq(self, seq):
        recoveries = []
        sessions = self.failure_types.get(seq)

        for session in sessions:
            _, tail = session.action_stream.rsplit('*', 1)
            if '$' in tail:
                recoveries.append(session)

        return recoveries

    def recoveries_by_seq_pct(self, seq):
        recoveries = self.recoveries_by_seq(seq)
        failures = self.failure_types[seq]
        return len(recoveries) / len(failures) * 100

    def report(self):
        return {
            # Basic Questions
            'basic': {
                'sessions': len(self.sessions),
                'sessions failed': len(self.failed_sessions),
                'sessions paid': len(self.paid_sessions),
                'when': (self.sessions[0].created_at, self.sessions[-1].created_at)
            },

            # Intermediate Questions
            'intermediate': {
                'unique users': len(self.users),
                'users paid': len(self.paid_users),
                'users failed': len(self.failed_users),
                'users failed then paid': len(self.failed_paid_users),
                'payments attempted': self.payments_attempted,
                'payments failed': self.payments_failed,
                'payment failed %': self.payments_failed / self.payments_attempted * 100,
                'user failed %': self.users_failed_pct
            },

            # Advanced Questions
            'advanced': {
                'user with most sessions': self.user_with_most_sessions,
                'invalid sessions': self.invalid_sessions,
                'failure types': dict([(k, len(v)) for (k,v) in self.failure_types.items()]),
                'recoveries post-P*H': self.recoveries_by_seq_pct(('P', 'H')),
                'recoveries post-P*B': self.recoveries_by_seq_pct(('P', 'B'))
            }
        }
