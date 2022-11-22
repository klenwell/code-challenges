class User:
    def __init__(self, id, sessions):
        self.id = id
        self.sessions = sessions

    def paid(self):
        for session in self.sessions:
            if '$' in session.action_stream:
                return True
        return False

    def failed(self):
        for session in self.sessions:
            if '*' in session.action_stream:
                return True
        return False

    def failed_then_paid(self):
        if not self.failed():
            return False
        return self.paid()

    def __repr__(self):
        f = '<User id={} sessions={}>'
        return f.format(self.id, len(self.sessions))
