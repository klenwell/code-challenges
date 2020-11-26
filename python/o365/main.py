from O365 import Account, MSGraphProtocol
from datetime import datetime
from pathlib import Path

from secrets import CLIENT_ID, SECRET_ID
from models.billable_event import BillableEvent


#
# Constants
#
SCOPES = ['Calendars.Read', 'Mail.Read']


#
# Commands
#
def calendar_events():
    """Based on
    https://medium.com/@pietrowicz.eric/how-to-read-microsoft-outlook-calendars-with-python-bdf257132318
    """
    account = authenticate()
    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    #start_date = datetime(2020, 1, 1)
    #end_date = datetime(2020, 12, 31)
    #q = calendar.new_query('start').greater_equal(start_date)
    #q.chain('and').on_attribute('end').less_equal(end_date)
    #events = calendar.get_events(query=q, include_recurring=True)
    events = calendar.get_events(include_recurring=False)
    events = list(events)
    event = events[0]

    print(len(events))
    print(events)
    #print(event.attendees[0].address)

    return events


def email_messages():
    """Based on
    https://github.com/O365/python-o365#mailbox
    """
    account = authenticate()
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    inbox_messages = list(inbox.get_messages())
    print(len(inbox_messages))

    sent_folder = mailbox.sent_folder()
    sent_messages = list(sent_folder.get_messages())
    print(len(sent_messages))

    messages = inbox_messages + sent_messages
    message = messages[0]

    print(len(messages))
    print(messages)
    print(message.to_api_data().keys())
    #print(message.to[0].address)

    return messages


#
# Helper Methods
#
def authenticate():
    credentials = (CLIENT_ID, SECRET_ID)
    protocol = MSGraphProtocol()
    account = Account(credentials, protocol=protocol)

    if account.is_authenticated:
        print("Token file exists!")
        # account.connection.refresh_token()
    else:
        account.authenticate(scopes=SCOPES)
        print('Authenticated!')

    return account


#
# Main Block
#
events = calendar_events()
messages = email_messages()
billable_events = [BillableEvent.from_calendar_event(event) for event in events]
billable_messages = [BillableEvent.from_email_message(message) for message in messages]
billables = billable_events + billable_messages
print(billables)
print(len(billables))
breakpoint()
