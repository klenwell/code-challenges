"""
A client is reporting some issues with one of their payment
flows. They're seeing an unusually high numbers of failed
payments. They've asked you to investigate by reviewing some
session logs they sent over as a serialized JSON array.

The log format was invented by a clever engineer years ago who
is no longer around. All the client knows about the format is:

- Each log represents a user session
- First 10 chars are a timestamp
- Next 9 chars are a user id
- Remaining chars represent a sequence of user page visits in the payment flow
- In payment flow string:
  - $ = successful payment
  - * = failed payment request
  - each letter is a page visit

Examples:

- Successful Payment Attempt: 1667203254504501499LHBP$B
- Failed Payment Attempt: 1667206315385842484LHBP*B

To get started, please answer the following questions:

- How many sessions are in the logs?
- How many users succeeded in making a payment?
- How many users failed to make a payment?
- On what date(s) did they visit?

JSON data:

'["1667204102094044579LHBP$BP$B", "1667204413379890628LHBP$BP$B", "1667204475270116745LHBP$B", "1667204657996534504LHBP$B", "1667204740653623688LHBP$B", "1667205206577719717LHBP$BP$BP$B", "1667206467691916051LHBP*HBP*H", "1667206698086544228LHBP$BP$B", "1667207060978414629LHBP$B", "1667207884633738705LHBP$B", "1667208243971550073LHBP$BP$BP$B", "1667208532599459231LHBP*BCBP$B", "1667208616827764334LHBP$B", "1667209239867413504LHBP$B", "1667209297447362969LHBP$B", "1667209305231823779LHBP$B", "1667209345447362969LHBP*H", "1667209420447362969LHBP$B", "1667209529447362969LHBP$B", "1667209540703623142LHBP$B", "1667209570447362969LHBP$B", "1667209672911572974LHBP*BCBP$B", "1667209688447362969LHBP$B", "1667209734447362969LHBP$B", "1667210978516414472LHBP*H", "1667211537516414472LHCBP$B", "1667212443844016588LHBP$B", "1667212671173773251LHBP$BP$B", "1667212689471147783LHBP*HBP*HCBP$B", "1667213302060102025LHBP$B", "1667213898LHBP*H", "1667214153568918505LHBP*H", "1667214638628241782LHBP$B", "1667215104256041080LHBP$B", "1667215982500028095LHBP*HCBP$B", "1667217223436643259LHBP*H", "1667217436679157913LHBP*H", "1667217802949650083LHBP$B", "1667218028501152501LHBP*H", "1667218325501152501LHBP*H", "1667218827113878690LHBP*B", "1667218920974940957LHBP$BP$B", "1667219437889684806LHBP*HBP*H", "1667219509183705196LHBP*H", "1667219977377666902LHBP$B", "1667220152937575930LHBP$B", "1667221291LHBP*H", "1667221498414294156LHBP*BCBP$B", "1667222341731284690LHBP*BCBP$B", "1667222386893200507LHBP*HBP*H", "1667222494410656487LHBP$BP$BP$BP$BP$BP$B", "1667223074024870733LHBP$B", "1667223144241372188LHBP*H", "1667223214286068152LHBP$B", "1667224113685967678LHBP$B", "1667224250992113092LHBP$B", "1667224254258325411LHBP*BCBP$B", "1667224430079133501LHBP$B", "1667224534488552136LHBP*B"]'
"""
import json
from datetime import datetime


#
# Data
#
json_logs = '["1667204102094044579LHBP$BP$B", "1667204413379890628LHBP$BP$B", "1667204475270116745LHBP$B", "1667204657996534504LHBP$B", "1667204740653623688LHBP$B", "1667205206577719717LHBP$BP$BP$B", "1667206467691916051LHBP*HBP*H", "1667206698086544228LHBP$BP$B", "1667207060978414629LHBP$B", "1667207884633738705LHBP$B", "1667208243971550073LHBP$BP$BP$B", "1667208532599459231LHBP*BCBP$B", "1667208616827764334LHBP$B", "1667209239867413504LHBP$B", "1667209297447362969LHBP$B", "1667209305231823779LHBP$B", "1667209345447362969LHBP*H", "1667209420447362969LHBP$B", "1667209529447362969LHBP$B", "1667209540703623142LHBP$B", "1667209570447362969LHBP$B", "1667209672911572974LHBP*BCBP$B", "1667209688447362969LHBP$B", "1667209734447362969LHBP$B", "1667210978516414472LHBP*H", "1667211537516414472LHCBP$B", "1667212443844016588LHBP$B", "1667212671173773251LHBP$BP$B", "1667212689471147783LHBP*HBP*HCBP$B", "1667213302060102025LHBP$B", "1667213898LHBP*H", "1667214153568918505LHBP*H", "1667214638628241782LHBP$B", "1667215104256041080LHBP$B", "1667215982500028095LHBP*HCBP$B", "1667217223436643259LHBP*H", "1667217436679157913LHBP*H", "1667217802949650083LHBP$B", "1667218028501152501LHBP*H", "1667218325501152501LHBP*H", "1667218827113878690LHBP*B", "1667218920974940957LHBP$BP$B", "1667219437889684806LHBP*HBP*H", "1667219509183705196LHBP*H", "1667219977377666902LHBP$B", "1667220152937575930LHBP$B", "1667221291LHBP*H", "1667221498414294156LHBP*BCBP$B", "1667222341731284690LHBP*BCBP$B", "1667222386893200507LHBP*HBP*H", "1667222494410656487LHBP$BP$BP$BP$BP$BP$B", "1667223074024870733LHBP$B", "1667223144241372188LHBP*H", "1667223214286068152LHBP$B", "1667224113685967678LHBP$B", "1667224250992113092LHBP$B", "1667224254258325411LHBP*BCBP$B", "1667224430079133501LHBP$B", "1667224534488552136LHBP*B"]'


#
# Basic Questions
#
def parse_log(logs):
    entries = json.loads(logs)
    return [(int(e[:10]), e[10:19], e[19:], e) for e in entries]


def session_span(sessions):
    sorted_sessions = sorted(sessions, key=lambda s: s[0])
    first_session = datetime.fromtimestamp(int(sorted_sessions[0][0]))
    last_session = datetime.fromtimestamp(int(sorted_sessions[-1][0]))
    return (first_session, last_session)


def basic():
    sessions = parse_log(json_logs)
    success_sessions = [s for s in sessions if '$' in s[-1]]
    failure_sessions = [s for s in sessions if '*' in s[-1]]

    return {
        'sessions': len(sessions),
        'sessions_success': len(success_sessions),
        'sessions_failed': len(failure_sessions),
        'dates': session_span(sessions)
    }


#
# Intermediate Questions
#
"""
Questions:

- How many unique users were logged?
- How many users succeeded in making a payment?
- How many users failed to make a payment?
- What percentage of payments failed?
- What percentage of users failed to make a payment?
"""
def parse_log_v2(logs):
    sessions = []
    entries = json.loads(logs)
    for e in entries:
        dt = datetime.fromtimestamp(int(e[:10]))
        try:
            session = (dt, int(e[10:19]), e[19:], e)
        except Exception as err:
            # print(err, e)
            session = (dt, '', e[10:], e)
        finally:
            sessions.append(session)
    return sessions


def extract_users(sessions):
    users = {}
    for session in sessions:
        uid = session[1]
        if uid in users:
            users[uid].append(session)
        else:
            users[uid] = [session]
    return users


def user_paid(sessions):
    for session in sessions:
        if '$' in session[2]:
            return True
    return False


def user_failed(sessions):
    for session in sessions:
        if '*' in session[2]:
            return True
    return False


def users_paid(users):
    paid = []
    for uid, sessions in users.items():
        if user_paid(sessions):
            paid.append(uid)
    return paid


def users_failed(users):
    failed = []
    for uid, sessions in users.items():
        if user_failed(sessions):
            failed.append(uid)
    return failed


def users_failed_then_succeeded(users):
    failed_success = []
    for uid, sessions in users.items():
        if not user_failed(sessions):
            continue
        if user_paid(sessions):
            failed_success.append(uid)
    return failed_success


def payment_counts(sessions):
    payment_counts = {
        'attempts': 0,
        'succeess': 0,
        'failure': 0
    }

    for _, _, flow, _ in sessions:
        payment_counts['succeess'] += flow.count('$')
        payment_counts['failure'] += flow.count('*')

    payment_counts['attempts'] = payment_counts['succeess'] + payment_counts['failure']
    return payment_counts


def intermediate():
    sessions = parse_log_v2(json_logs)
    users = extract_users(sessions)

    uniq_users = len(users.keys())
    paid_users = len(users_paid(users))
    failed_users = len(users_failed(users))
    failed_then_paid_users = len(users_failed_then_succeeded(users))
    pay_counts = payment_counts(sessions)
    user_fail_pct = (failed_users - failed_then_paid_users) / uniq_users * 100

    return {
        'sessions': len(sessions),
        'unique-users': uniq_users,
        'users-paid': paid_users,
        'users-failed': failed_users,
        'user-failed-then-paid': failed_then_paid_users,
        'payment-attempts': pay_counts['attempts'],
        'payment-failures': pay_counts['failure'],
        'payment-failure-pct': pay_counts['failure'] / pay_counts['attempts'] * 100,
        'user-failure-pct': user_fail_pct
    }


#
# Advanced
#
"""
Questions:

- What user had the most sessions?
- Do you see any interesting patterns in the data?
- Do you have any hypotheses regarding the problem?
- What do you recommend for next steps?
"""
class Session():
    def __init__(self, log):
        self.timestamp = log[:10]
        self.log = log

    @property
    def created_at(self):
        return datetime.fromtimestamp(int(self.timestamp))

    @property
    def user_id(self):
        return self.log[10:19]

    @property
    def flow(self):
        return self.log[19:]

    def is_valid(self):
        try:
            self.validate()
            return True
        except AssertionError as e:
            self.error = e
            return False

    def validate(self):
        assert(self.user_id.isdigit())
        assert(self.created_at.__class__ is datetime)

    def __repr__(self):
        f = '<Session created_at={} user_id={} flow={}>'
        return f.format(self.created_at, self.user_id, self.flow)



class User():
    def __init__(self, session):
        self.id = session.user_id
        self.sessions = [session]

    def add_session(self, session):
        self.sessions.append(session)
        return self

    def __repr__(self):
        f = '<User id={} sessions={}>'
        return f.format(self.id, len(self.sessions))


def parse_log_v3(serialized_logs):
    sessions = []
    logs = json.loads(serialized_logs)
    for log in logs:
        session = Session(log)
        sessions.append(session)
    return sessions


def extract_users_v2(sessions):
    users = {}
    for session in sessions:
        if session.user_id in users:
            users[session.user_id].add_session(session)
        else:
            users[session.user_id] = User(session)
    return users.values()


def extract_failure_types(sessions):
    types = {}
    for session in sessions:
        if not '*' in session.flow:
            continue
        for i, char in enumerate(session.flow):
            if char == '*':
                before = session.flow[i-1]
                after = session.flow[i+1]
                if (before, after) in types:
                    types[(before, after)].append(session)
                else:
                    types[(before, after)] = [session]
    return types


def extract_recoveries(sessions, seq):
    recoveries = []
    sessions = extract_failure_types(sessions).get(seq)

    for session in sessions:
        _, tail = session.flow.rsplit('*', 1)
        if '$' in tail:
            recoveries.append(session)

    return recoveries


def advanced():
    sessions = parse_log_v3(json_logs)
    users = extract_users_v2(sessions)

    invalid_sessions = [s for s in sessions if not s.is_valid()]
    failure_types = extract_failure_types(sessions)
    ph_recoveries = extract_recoveries(sessions, ('P', 'H'))
    pb_recoveries = extract_recoveries(sessions, ('P', 'B'))

    return {
        'most-user-sessions': sorted(users, key=lambda u: len(u.sessions))[-1],
        'invalid-sessions': invalid_sessions,
        'failure-types': dict([(k, len(v)) for (k,v) in failure_types.items()]),
        'recoveries-post-P*H': len(ph_recoveries) / len(failure_types[('P', 'H')]) * 100,
        'recoveries-post-P*B': len(pb_recoveries) / len(failure_types[('P', 'B')]) * 100
    }


#
# Main
#
def main():
    print(basic())
    print(intermediate())
    print(advanced())


main()
