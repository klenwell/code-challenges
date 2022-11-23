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
- How many sessions saw a payment fail?
- How many sessions saw a payment succeed?
- On what date(s) did the sessions occur?

JSON data:

'["1667204102094044579LHBP$BP$B", "1667204413379890628LHBP$BP$B", ...]'
"""
from pprint import pprint
from puzzler import Puzzler
from solver import Solver


def new():
    puzzle = Puzzler.construct()
    solution = Solver.solve(puzzle.serialized_logs)
    pprint(puzzle.report())
    pprint(solution.report())
    #print(puzzle.to_file())


def existing():
    input = ''
    solution = Solver.solve(input)
    pprint(solution.report())


def main():
    new()
    #existing()


main()
