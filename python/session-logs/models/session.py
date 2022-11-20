from random import randint, choice, shuffle
from datetime import datetime


class Session:
    @staticmethod
    def successful_payment(*args):
        payments = args[0]
        timestamp = args[1]
        session = Session(timestamp)
        session.login().home().pay()

        for n in range(payments - 1):
            session.pay()

        session.clean()
        return [session]

    @staticmethod
    def bad_card_success(*args):
        timestamp = args[0]
        session = Session(timestamp)
        session.login().home().pay_fail().card().pay()
        return [session]

    @staticmethod
    def bad_card_failure(*args):
        timestamp = args[0]
        session = Session(timestamp)
        session.login().home().pay_fail()
        return [session]

    @staticmethod
    def bug_expired_card_failure(*args):
        timestamp = args[0]
        session = Session(timestamp)
        session.login().home().pay_bug()

        for n in range(choice([0, 0, 0, 1, 1, 2])):
            session.pay_bug()

        return [session]

    @staticmethod
    def bug_expired_card_success(*args):
        timestamp = args[0]
        session = Session(timestamp)
        session.login().home().pay_bug()

        for n in range(choice([0, 0, 0, 1, 1, 2])):
            session.pay_bug()

        session.card().pay()
        return [session]

    @staticmethod
    def bug_expired_card_relogin_success(*args):
        # Session 1
        timestamp = args[0]
        session1 = Session(timestamp)
        session1.login().home().pay_bug()

        # Session 2
        session2 = Session(timestamp + randint(200, 600))
        session2.login().home().card().pay()
        session2.uid = session1.uid
        return [session1, session2]

    @staticmethod
    def bug_expired_card_relogin_failure(*args):
        # Session 1
        timestamp = args[0]
        session1 = Session(timestamp)
        session1.login().home().pay_bug()

        # Session 2
        session2 = Session(timestamp + randint(30, 300))
        session2.login().home().pay_bug()
        session2.uid = session1.uid
        return [session1, session2]

    @staticmethod
    def scammer(*args):
        pay_successes, pay_failures, timestamp = args
        results = ([1] * pay_successes) + ([0] * pay_failures)
        shuffle(results)

        sessions = []
        original_session = Session(timestamp)
        uid = original_session.uid

        for result in results:
            timestamp = timestamp + randint(20, 120)
            session = Session(timestamp)

            if result == 1:
                session.login().home().pay_bug()
            else:
                session.login().home().pay()

            session.uid = uid
            sessions.append(session)

        return sessions

    @staticmethod
    def invalid(*args):
        timestamp = args[0]
        session = InvalidSession(timestamp)
        session.login().home().pay_bug()
        return [session]

    def __init__(self, timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now().timestamp()
        self.uid =randint(1, 999999999)
        self.action_stream = ''

    def to_log(self):
        f = '{}{:09d}{}'
        return f.format(self.timestamp, self.uid, self.action_stream)

    #
    # Action Stream Actions
    #
    def login(self):
        self.action_stream += 'L'
        return self

    def home(self):
        self.action_stream += 'H'
        return self

    def pay(self):
        self.action_stream += 'BP$B'
        return self

    def pay_fail(self):
        self.action_stream += 'BP*B'
        return self

    def pay_bug(self):
        self.action_stream += 'BP*H'
        return self

    def card(self):
        self.action_stream += 'C'
        return self

    def clean(self):
        self.action_stream = self.action_stream.replace('BB', 'B')
        return self


class InvalidSession(Session):
    def to_log(self):
        return '{}{}'.format(self.timestamp, self.action_stream)
