"""
A client is reporting some issues with one of their payment flows. They're seeing
an unusally high numbers of failed payments. They've asked you to investigate by
reviewing some logs they sent over.

Regrettably, a really clever engineer created his own log format years ago. You've
been asked to parse them. All your client knows about the format is:

- Each log represents a user session
- First 10 chars are a timestamp
- Next 9 chars are a user id
- Remain characters represent a sequence of user page visits in the payment flow
- In payment flow string:
  - $ = successful payment
  - * = failed payment request
  - letters are different sites pages or views

It's our own proprietry format: timestamp(10)|uid(9)|pageseq(var)
"""
import json
import base64
from datetime import datetime, timedelta
from random import randint
from models.session_log import SessionLog

START_DATE_TIME = (2022, 10, 31, 1)
DURATION = 6  # hours

SESSIONS = [
    # method, args, count
    (SessionLog.happy_payment, [1], 21),
    (SessionLog.happy_payment, [2], 5),
    (SessionLog.happy_payment, [3], 2),
    (SessionLog.happy_payment, [6], 1),
    (SessionLog.bad_card_success, [], 5),
    (SessionLog.bad_card_failure, [], 2),
    (SessionLog.bug_expired_card_failure, [], 8),
    (SessionLog.bug_expired_card_success, [], 2),
    (SessionLog.bug_expired_card_relogin_success, [], 1),
    (SessionLog.bug_expired_card_relogin_failure, [], 1),
    (SessionLog.scammer, [1, 6], 1),
    (SessionLog.invalid, [], 2),
]


def generate(sessions, start_at, duration):
    end_by = start_at + timedelta(hours=DURATION)
    unix_start_at = int(start_at.timestamp())
    unix_end_by = int(end_by.timestamp())

    # print(unix_start_at, unix_end_by)

    session_logs = []
    for method, args, count in sessions:
        print(method, args)
        args.append(unix_start_at)
        for n in range(count):
            timestamp = randint(unix_start_at, unix_end_by)
            args.pop()
            args.append(timestamp)
            session_logs += method(*args)
        print(len(session_logs))

    session_logs.sort()
    return json.dumps(session_logs)


def test_log(serialized_log):
    logs = json.loads(serialized_log)
    sessions = [(log[:10], log[10:19], log[19:]) for log in logs]
    sessions = sorted(sessions, key=lambda s: s[0])

    started_at = sessions[0][0]
    ended_at = sessions[-1][0]
    hours = (int(ended_at) - int(started_at)) / 3600

    invalid_sessions = [session for session in sessions if not session[1].isdigit()]
    valid_sessions = [s for s in sessions if s[1].isdigit()]
    failed_sessions = [s for s in sessions if '*' in s[2]]
    successful_sessions = [s for s in sessions if '$' in s[2]]

    users = set([session[1] for session in sessions])
    valid_users = set([session[1] for session in valid_sessions])

    successful_payments = 0
    failed_payments = 0
    for log in logs:
        successful_payments += log.count('$')
        failed_payments += log.count('*')
    payment_attempts = successful_payments + failed_payments

    return {
        'sessions': len(sessions),
        'hours': hours,
        'sessions_per_hour': len(sessions) / hours,
        'users': len(users),
        'valid_users': len(valid_users),
        'successes': len(successful_sessions),
        'failures': len(failed_sessions),
        'valid_sessions': len(valid_sessions),
        'invalid_sessions': len(invalid_sessions),
        'payment_attempts': payment_attempts,
        'successful_payments': successful_payments,
        'failed_payments': failed_payments,
        'success %': successful_payments / payment_attempts * 100
    }


def main():
    serialized_log = generate(SESSIONS, datetime(*START_DATE_TIME), DURATION)
    results = test_log(serialized_log)
    print(results)

    #encoded_log = str(base64.b64encode(serialized_log.encode()), 'ascii')
    #print((serialized_log[:20],  type(serialized_log), len(serialized_log)),
    #      (encoded_log[:20],  type(encoded_log), len(encoded_log)))
    print(serialized_log)
    #breakpoint()

#
# Main
#
main()
