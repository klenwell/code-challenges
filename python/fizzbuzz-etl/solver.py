class Solver:
    @staticmethod
    def solve(encoded_logs):
        return Solver(encoded_logs)

    def __init__(self, encoded_logs):
        self.encoded_logs = encoded_logs

    def report(self):
        return {}
