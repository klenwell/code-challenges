from random import randint, choice, shuffle
from datetime import datetime


class Session:
    #
    # Generators
    #
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
        session2.user_id = session1.user_id
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
        session2.user_id = session1.user_id
        return [session1, session2]

    @staticmethod
    def scammer(*args):
        pay_successes, pay_failures, timestamp = args
        results = ([1] * pay_successes) + ([0] * pay_failures)
        shuffle(results)

        sessions = []
        original_session = Session(timestamp)
        user_id = original_session.user_id

        for result in results:
            timestamp = timestamp + randint(20, 120)
            session = Session(timestamp)

            if result == 1:
                session.login().home().pay_bug()
            else:
                session.login().home().pay()

            session.user_id = user_id
            sessions.append(session)

        return sessions

    @staticmethod
    def invalid(*args):
        timestamp = args[0]
        session = InvalidSession(timestamp)
        session.login().home().pay_bug()
        return [session]

    @staticmethod
    def from_log(log):
        """Note: this does not validate."""
        timestamp = log[:10]
        session = Session(timestamp)
        session.user_id = log[10:19]
        session.action_stream = log[19:]
        return session

    #
    # Instance Methods
    #
    def __init__(self, timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now().timestamp()
        self.user_id =randint(1, 999999999)
        self.action_stream = ''
        self.error = None

    def to_log(self):
        f = '{}{:09d}{}'
        return f.format(self.timestamp, self.user_id, self.action_stream)

    def paid(self):
        return '$' in self.action_stream

    def failed(self):
        return '*' in self.action_stream

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

    @property
    def payments_attempted(self):
        return self.payments_succeeded + self.payments_failed

    @property
    def payments_succeeded(self):
        return self.action_stream.count('$')

    @property
    def payments_failed(self):
        return self.action_stream.count('*')

    @property
    def created_at(self):
        if not self.timestamp:
            return None
        return datetime.fromtimestamp(int(self.timestamp))

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

    def __repr__(self):
        f = '<Session created_at={} user_id={} actions={}>'
        return f.format(self.created_at, self.user_id, self.action_stream)


class InvalidSession(Session):
    def to_log(self):
        return '{}{}'.format(self.timestamp, self.action_stream)
