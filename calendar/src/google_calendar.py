import os
import json
import dotenv
from pathlib import Path
from pprint import pprint
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

dotenv.load_dotenv(Path(__file__).parent / 'env')
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = Path(os.environ['CREDENTIALS_PATH'])
GCP_DIR = CREDENTIALS_PATH.parent


def get_service():
    creds = None
    if (GCP_DIR / 'token.json').exists():
        creds = Credentials.from_authorized_user_file(GCP_DIR / 'token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(GCP_DIR / 'token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_calendar_events(num: int = 10):
    service = get_service()
    now = datetime.now().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=num, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')

    event_list = []
    for event in events:
        # jsonに変換
        event_list.append(dict(event))
    return event_list

def add_calendar_event_timeboxed(
        event_name: str,
        start_time: str,
        end_time: str,
        description: str = "",
        location: str = ""
    ) -> None:
    """
    時間指定の予定を追加 (start_time/end_timeは "YYYY-MM-DDTHH:MM:SS" 形式)
    """
    service = get_service()
    event = {
        'summary': event_name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Tokyo',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    result_str = f"Event created: {event.get('htmlLink')}"
    print(result_str)
    return result_str

def add_calendar_event_allday(
        event_name: str,
        start_date: str,
        end_date: str,
        description: str = "",
        location: str = ""
    ) -> None:
    """
    終日の予定を追加 (dateは "YYYY-MM-DD" 形式)
    """
    service = get_service()
    event = {
        'summary': event_name,
        'location': location,
        'description': description,
        'start': {
            'date': start_date,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'date': end_date,
            'timeZone': 'Asia/Tokyo',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    result_str = f"All-day event created: {event.get('htmlLink')}"
    print(result_str)
    return result_str

def main():
    pprint(get_calendar_events())

    # add_calendar_event_timeboxed(
    #     event_name="test event",
    #     start_time="2025-06-05T09:00:00",
    #     end_time="2025-06-05T10:00:00",
    #     location="Tokyo",
    #     description="test"
    # )

    # add_calendar_event_allday(
    #     event_name="whole day event",
    #     date="2025-06-06",
    #     location="大阪",
    #     description="allday"
    # )

if __name__ == '__main__':
    main()