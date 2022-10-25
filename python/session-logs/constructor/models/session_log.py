from random import randint, choice
from datetime import datetime

class SessionLog():
    @staticmethod
    def happy_payment(*args):
        payments = args[0]
        timestamp = args[1]
        log = SessionLog(timestamp)
        log.login().home().pay()

        for n in range(payments - 1):
            log.pay()

        log.clean()

        return [str(log)]

    @staticmethod
    def bad_card_success(*args):
        timestamp = args[0]
        log = SessionLog(timestamp)
        log.login().home().pay_fail().card().pay()
        return [str(log)]

    @staticmethod
    def bad_card_failure(*args):
        timestamp = args[0]
        log = SessionLog(timestamp)
        log.login().home().pay_fail()
        return [str(log)]

    @staticmethod
    def bug_expired_card_failure(*args):
        timestamp = args[0]
        log = SessionLog(timestamp)
        log.login().home().pay_bug()

        for n in range(choice([0, 0, 0, 1, 1, 2])):
            log.pay_bug()

        return [str(log)]

    @staticmethod
    def bug_expired_card_success(*args):
        return []

    @staticmethod
    def bug_expired_card_relogin_success(*args):
        return []

    @staticmethod
    def bug_expired_card_relogin_failure(*args):
        return []

    @staticmethod
    def scammer(*args):
        return []

    @staticmethod
    def invalid(*args):
        return []

    def __init__(self, timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now().timestamp()
        self.uid =randint(1, 999999999)
        self.action_stream = ''

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

    def __str__(self):
        f = '{}{:09d}{}'
        return f.format(self.timestamp, self.uid, self.action_stream)
