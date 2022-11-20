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

'["1667204102094044579LHBP$BP$B", "1667204413379890628LHBP$BP$B", "1667204475270116745LHBP$B", "1667204657996534504LHBP$B", "1667204740653623688LHBP$B", "1667205206577719717LHBP$BP$BP$B", "1667206467691916051LHBP*HBP*H", "1667206698086544228LHBP$BP$B", "1667207060978414629LHBP$B", "1667207884633738705LHBP$B", "1667208243971550073LHBP$BP$BP$B", "1667208532599459231LHBP*BCBP$B", "1667208616827764334LHBP$B", "1667209239867413504LHBP$B", "1667209297447362969LHBP$B", "1667209305231823779LHBP$B", "1667209345447362969LHBP*H", "1667209420447362969LHBP$B", "1667209529447362969LHBP$B", "1667209540703623142LHBP$B", "1667209570447362969LHBP$B", "1667209672911572974LHBP*BCBP$B", "1667209688447362969LHBP$B", "1667209734447362969LHBP$B", "1667210978516414472LHBP*H", "1667211537516414472LHCBP$B", "1667212443844016588LHBP$B", "1667212671173773251LHBP$BP$B", "1667212689471147783LHBP*HBP*HCBP$B", "1667213302060102025LHBP$B", "1667213898LHBP*H", "1667214153568918505LHBP*H", "1667214638628241782LHBP$B", "1667215104256041080LHBP$B", "1667215982500028095LHBP*HCBP$B", "1667217223436643259LHBP*H", "1667217436679157913LHBP*H", "1667217802949650083LHBP$B", "1667218028501152501LHBP*H", "1667218325501152501LHBP*H", "1667218827113878690LHBP*B", "1667218920974940957LHBP$BP$B", "1667219437889684806LHBP*HBP*H", "1667219509183705196LHBP*H", "1667219977377666902LHBP$B", "1667220152937575930LHBP$B", "1667221291LHBP*H", "1667221498414294156LHBP*BCBP$B", "1667222341731284690LHBP*BCBP$B", "1667222386893200507LHBP*HBP*H", "1667222494410656487LHBP$BP$BP$BP$BP$BP$B", "1667223074024870733LHBP$B", "1667223144241372188LHBP*H", "1667223214286068152LHBP$B", "1667224113685967678LHBP$B", "1667224250992113092LHBP$B", "1667224254258325411LHBP*BCBP$B", "1667224430079133501LHBP$B", "1667224534488552136LHBP*B"]'
"""
from pprint import pprint
from puzzler import Puzzler
from solver import Solver


def new():
    puzzle = Puzzler.construct()
    solution = Solver.solve(puzzle.serialized_logs)
    pprint(puzzle.report())
    pprint(solution.report())
    print(puzzle.to_file())


def existing():
    input = ''
    solution = Solver.solve()
    pprint(solution.report())


def main():
    new()
    #existing()


main()
