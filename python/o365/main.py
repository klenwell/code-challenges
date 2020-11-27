from datetime import date, timedelta
from secrets import CLIENT_ID, SECRET_ID
from services.business_activity_service import BusinessActivityService


#
# Main Method
#
def main():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    activities = service.fetch_activities()
    print(len(activities))
    breakpoint()

def activities():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    activities = service.fetch_activities()
    print(len(activities))
    breakpoint()

def data_types():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    end = date.today()
    start = end - timedelta(days=7)

    emails = service.fetch_emails(start, end)
    meetings = service.fetch_meetings(start, end)
    breakpoint()


#
# Main Block
#
main()
