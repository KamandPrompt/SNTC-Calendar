from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

class CalenderEventsUtil():
    scopes = ["https://www.googleapis.com/auth/calendar"]

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    token_uri = "https://oauth2.googleapis.com/token"

    # User related OAuth tokens
    access_token = None
    refresh_token = None

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def create_event_data(
            self,
            summary,
            location,
            description,
            start_data_time,
            end_date_time,
            attendees_emails,
            reminders_default=False,
            timezone='Asia/Kolkata'):
        """
        Create event data dict that allows google calender to create events
        DateTime format Example - '2022-10-06T17:30:00'
        attendies - emails for attendies
        """
        if location is None:
            location = ''
        
        if description is None:
            description = ''

        reminders = {'useDefault': True}

        if not reminders_default:
            reminders = {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ]}

        attendees_list = []
        if attendees_emails:
            for attendee in attendees_emails:
                attendees_list.append({'email': attendee})

        return {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_data_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime':end_date_time,
                'timeZone': timezone,
            },
            'attendees': attendees_list,
            'reminders': reminders
        }

    def get_calender_service(self):
        ''' Uses credentials from global to create credential service '''

        creds = Credentials(
            self.access_token,
            refresh_token=self.refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes
        )

        service = build('calendar', 'v3', credentials=creds)
        return service

    def create_calender_event(self, event_data):
        '''
        Create calender event
        @params event_data - The event dict as comes form `create_event_data`
        '''

        try:
            service = self.get_calender_service()
            event = service.events().insert(calendarId='primary', body=event_data).execute()
            event_link = event.get('htmlLink')
            event_id = event.get('id')

            print('Event created: ', event_link, event_id)
            return {
                'success': True,
                'event_link': event_link,
                'event_id': event_id
            }

        except Exception as e:
            print("Exception came while creating event: ", e)
            return {
                'success': False,
                'error': e
            }

    def retrieve_calender_event(self, event_id):
        try:
            service = self.get_calender_service()
            event = service.events().get(calendarId='primary', eventId=event_id).execute()

            return {
                'success': True,
                'event_link': event.get('htmlLink'),
                'event_id': event_id,
                'summary': event.get('summary')
            }

        except Exception as e:
            print("Exception came while creating event: ", e)
            return {
                'success': False,
                'error': e
            }

    def update_calender_event(self, event_id, event_data):
        # First retrieve the event from the API.
        try:
            service = self.get_calender_service()
            event = service.events().get(calendarId='primary', eventId=event_id).execute()

            for key in event_data:
                event[key] = event_data[key]

            updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            return {
                'success': True,
                'event_link': updated_event.get('htmlLink'),
                'event_id': event_id
            }

        except Exception as e:
            print("Exception came while creating event: ", e)
            return {
                'success': False,
                'error': e
            }

    def delete_calender_event(self, event_id):
        ''' Deletes the specified calender event from google calender '''

        try:
            service = self.get_calender_service()
            service.events().delete(calendarId='primary', eventId=event_id).execute()

            return {
                'success': True,
                'event_id': event_id
            }
        except Exception as e:
            print("Exception came while deleting the event: ", e)
            return {
                'success': False,
                'error': e
            }
