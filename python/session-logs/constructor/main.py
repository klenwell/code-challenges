"""
'["1667203472786351643LHBP$B", "1667203754520021531LHBP$B", "1667204690638492524LHBP$B", "1667205551252182275LHBP$B", "1667207687693856677LHBP$B", "1667207893813198027LHBP$B", "1667207991378831675LHBP$B", "1667208394990284308LHBP$B", "1667209898214212671LHBP$B", "1667209902985120989LHBP$B", "1667210306727135789LHBP$B", "1667210481916452736LHBP$B", "1667210518360277326LHBP$B", "1667211285100757812LHBP$B", "1667211437701388520LHBP$B", "1667211640896145439LHBP$B", "1667212545872017431LHBP$B", "1667214277417428555LHBP$B", "1667217586810068733LHBP$B", "1667217819383215013LHBP$B", "1667217889178441925LHBP$B", "1667218516263657257LHBP$B", "1667218754055350470LHBP$B", "1667220136940094742LHBP$B", "1667220263180744033LHBP$B", "1667220725601885947LHBP$B", "1667220968094888262LHBP$B", "1667220985279838369LHBP$B", "1667221712919010382LHBP$B"]'
"""
import json
from datetime import datetime, timedelta
from random import randint
from models.session_log import SessionLog

START_DATE_TIME = (2022, 10, 31, 1)
DURATION = 6  # hours

def main():
    sessions = [
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
    start_at = datetime(*START_DATE_TIME)
    end_by = start_at + timedelta(hours=DURATION)

    unix_start_at = int(start_at.timestamp())
    unix_end_by = int(end_by.timestamp())
    print(unix_start_at, unix_end_by)

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

    print(session_logs)
    session_logs.sort()

    json_array = json.dumps(session_logs)
    print(type(json_array), json_array)


#
# Main
#
main()
