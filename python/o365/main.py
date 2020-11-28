from datetime import date, timedelta
import csv
from secrets import CLIENT_ID, SECRET_ID
from services.business_activity_service import BusinessActivityService


#
# Main Method
#
def main():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    activities = service.fetch_activities()
    csv_path = write_to_csv(activities)
    print('Wrote {} activities to {}'.format(len(activities), csv_path))
    breakpoint()


def activities():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    activities = service.fetch_activities()
    print(len(activities))
    breakpoint()


def api_data():
    service = BusinessActivityService(CLIENT_ID, SECRET_ID)
    end = date.today()
    start = end - timedelta(days=7)

    emails = service.fetch_emails(start, end)
    meetings = service.fetch_meetings(start, end)
    breakpoint()


def write_to_csv(activities):
    csv_path = 'o365-activites-{}.csv'.format(date.today().strftime('%Y%m%d'))
    csv_header = ['Date', 'Type', 'Start', 'End', 'Title', 'Owner', 'Description']

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

        for activity in activities:
            writer.writerow(activity.to_csv())

    return csv_path


#
# Main Block
#
main()
