class User:
    def __init__(self, uid, sessions):
        self.uid = uid
        self.sessions = sessions

    def paid(self):
        for session in self.sessions:
            if '$' in session.action_stream:
                return True
        return False
