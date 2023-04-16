from __future__ import print_function
import requests

import datetime
import os.path
import string

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    setupCredentials()
    getEvents()

def setupCredentials():
    # https://developers.google.com/calendar/api/quickstart/python
    global creds
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def getEvents():     
    try:
        service = build('calendar', 'v3', credentials=creds)

        calendar_list = service.calendarList().list().execute()

        events_result = service.events().list(calendarId='primary', timeMin='2023-04-01T00:00:00-05:00', timeMax='2023-05-01T00:00:00-05:00',
                                              maxResults=50, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        eventData = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event['summary'].encode("charmap", "ignore").decode("utf-8")
            event_id = event["id"]
            print(start, summary, event_id)
            eventData.append([start, summary, event_id])
        
        print(len(eventData), "Google Calendar events received.")
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()