class BusinessActivity:
    def __init__(self, **params):
        self.resource = params.get('resource')
        self.owner = params.get('owner')
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
        return BusinessActivity(
            resource='email',
            owner=message.sender.address,
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
        return BusinessActivity(
            resource='meeting',
            owner=event.organizer.address,
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
    def to_csv(self):
        return [
            self.date,
            self.resource,
            self.started_at,
            self.ended_at,
            self.title,
            self.owner,
            self.description
        ]

    def __repr__(self):
        f_ = '<BusinessActivity ({}) title="{}" date={}>'
        return f_.format(self.resource, self.title, self.date)
