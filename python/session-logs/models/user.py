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

    @property
    def sessions_span(self):
        if len(self.sessions) < 2:
            return None
        sorted_sessions = sorted(self.sessions, key=lambda s: s.created_at)
        return sorted_sessions[-1].created_at - sorted_sessions[0].created_at

    def __repr__(self):
        f = '<User id={} sessions={}>'
        return f.format(self.id, len(self.sessions))
