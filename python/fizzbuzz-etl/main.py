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
- How many records had an incorrect computation?
- Which computation was miscalculated most frequently?

"""
import base64
from datetime import datetime, timedelta
from random import randint
from models.fizzer import FaultyFizzer


def main():
    """
    Create a series of random fizzers between given dates.
    """
    # Params
    count = 122
    start_date = datetime(2023, 1, 1)
    delim = '\n'

    # Fizzers
    fizzers = []
    start_ts = int(start_date.timestamp())
    end_ts = int((start_date + timedelta(days=7)).timestamp())

    # Generate
    for n in range(count):
        timestamp = randint(start_ts, end_ts)
        fizzer = FaultyFizzer(timestamp, .08)
        fizzers.append(fizzer)

    # Serialize
    serialized_fizzers = delim.join([f.to_s() for f in fizzer])
    encoded_str = str(base64.b64encode(serialized_log.encode()), 'ascii')

    # Report
    report = {
        'serial len': len(serialized_fizzers),
        'encoded_len': len(encoded_str),
        'encoded': encoded_str,
        'lines': (base64.b64decode(encoded_str).decode()).split(delim)
    }

#
# Main
#
main()
