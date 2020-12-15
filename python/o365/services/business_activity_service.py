"""
BusinessActivityService

A class for interfacing with business productivity service API. It is set up initally
to interface with Microsoft Office 365 API. But conceivably in the future it could
be updated to also interface or even be replaced by Google Workspace.
"""
from O365 import Account, MSGraphProtocol
from datetime import date, timedelta
from models.business_activity import BusinessActivity


SCOPES = ['Calendars.Read', 'Mail.Read']


class BusinessActivityService:
    def __init__(self, client_id, secret_id):
        self.client_id = client_id
        self.secret_id = secret_id
        self.account = self.authenticate()

    #
    # Properties
    #
    @property
    def mailbox(self):
        mailbox = self.account.mailbox()
        return mailbox

    @property
    def calendar(self):
        schedule = self.account.schedule()
        return schedule.get_default_calendar()

    #
    # Instance Methods
    #
    def fetch_activities(self, start_date=None, end_date=None):
        if not end_date:
            end_date = date.today()

        if not start_date:
            start_date = end_date - timedelta(days=7)

        emails = self.fetch_emails(start_date, end_date)
        meetings = self.fetch_meetings(start_date, end_date)

        meeting_activities = [
            BusinessActivity.from_calendar_event(meeting) for meeting in meetings]
        email_activities = [BusinessActivity.from_email_message(email) for email in emails]

        activities = meeting_activities + email_activities
        return sorted(activities, key=lambda a: a.started_at)

    def fetch_emails(self, start_date, end_date):
        """Based on
        https://github.com/O365/python-o365#mailbox

        https://docs.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0
        """
        inbox = self.mailbox.inbox_folder()
        q = inbox.new_query('sentDateTime').greater_equal(start_date)
        q.chain('and').on_attribute('sentDateTime').less_equal(end_date)
        inbox_messages = inbox.get_messages(query=q, limit=500)

        sent_folder = self.mailbox.sent_folder()
        q = sent_folder.new_query('sentDateTime').greater_equal(start_date)
        q.chain('and').on_attribute('sentDateTime').less_equal(end_date)
        sent_messages = sent_folder.get_messages(query=q, limit=500)

        return list(inbox_messages) + list(sent_messages)

    def fetch_meetings(self, start_date, end_date):
        """Based on
        https://medium.com/@pietrowicz.eric/how-to-read-microsoft-outlook-calendars-with-python-bdf257132318
        """
        q = self.calendar.new_query('start').greater_equal(start_date)
        q.chain('and').on_attribute('end').less_equal(end_date)
        events = self.calendar.get_events(query=q, include_recurring=True, limit=500)
        return list(events)

    def authenticate(self):
        credentials = (self.client_id, self.secret_id)
        protocol = MSGraphProtocol()
        account = Account(credentials, protocol=protocol)

        if account.is_authenticated:
            print("Token file exists!")
        else:
            authenticated = account.authenticate(scopes=SCOPES)
            if authenticated:
                print('Authenticated!')
            else:
                print('Failed to authenticate.')

        return account
