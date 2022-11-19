"""
New-line separated string, base64-encoded, of about 100 lines. Format:

- unix-timestamp
- fizzbuzz computation: <blank> | 'fizz' | 'buzz' | 'fizzbuzz'
- Computation is based on timestamp

Examples:
- `1668817445fizzbuzz`
- `1668817504`
- Encoded: `MTY2ODgxNzQ0NWZpenpidXp6CjE2Njg4MTc1MDQ=`

Questions:

- How many records are there?
- When were the records generated?
- What day of the week had the most 'fizzbuzz' computations?
- What is the error rate? (How many records had an incorrect computation?)
- Which computation was miscalculated most frequently?

"""
from pprint import pprint
from puzzler import Puzzler
from solver import Solver


def new():
    puzzle = Puzzler.construct()
    solution = Solver.solve(puzzle.encoded_logs)
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
