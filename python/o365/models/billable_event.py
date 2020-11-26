class BillableEvent:
    def __init__(self, **params):
        self.resource = params.get('resource')
        self.started_at = params.get('started_at')
        self.ended_at = params.get('started_at')
        self.created_at = params.get('created_at')
        self.title = params.get('title')
        self.description = params.get('description')
        self.url = params.get('url')
        self.data = params.get('data')

    #
    # Static Methods
    #
    @staticmethod
    def from_email_message(message):
        return BillableEvent(
            resource='email',
            started_at=message.sent,
            ended_at=message.received,
            created_at=message.created,
            title=message.subject,
            description=message.body_preview,
            url=message.web_link,
            data=message.to_api_data()
        )

    @staticmethod
    def from_calendar_event(event):
        return BillableEvent(
            resource='meeting',
            started_at=event.start,
            ended_at=event.end,
            created_at=event.created,
            title=event.subject,
            description=event.get_body_text(),
            url=None,
            data=event.to_api_data()
        )

    #
    # Properties
    #
    @property
    def date(self):
        return self.started_at.date()

    #
    # Instance Methods
    #
    def __repr__(self):
        f_ = "<BillableEvent ({}) title={} date={}>"
        return f_.format(self.resource, self.title, self.date)
