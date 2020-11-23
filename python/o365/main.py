from O365 import Account, MSGraphProtocol
from secrets import CLIENT_ID, SECRET_ID
from datetime import datetime


#
# Commands
#
def calendar_events():
    """Based on
    https://medium.com/@pietrowicz.eric/how-to-read-microsoft-outlook-calendars-with-python-bdf257132318
    """
    scopes = ['Calendars.Read']
    account = authenticate(scopes)

    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)
    q = calendar.new_query('start').greater_equal(start_date)
    q.chain('and').on_attribute('end').less_equal(end_date)

    events = calendar.get_events(query=q, include_recurring=True)
    events = list(events)

    print(len(events))
    print(events)
    breakpoint()


#
# Helper Methods
#
def authenticate(scopes):
    credentials = (CLIENT_ID, SECRET_ID)
    protocol = MSGraphProtocol()
    account = Account(credentials, protocol=protocol)

    if account.authenticate(scopes=scopes):
        print('Authenticated!')

    return account


#
# Main Block
#
calendar_events()
