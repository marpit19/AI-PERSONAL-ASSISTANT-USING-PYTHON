import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from spotify_local import SpotifyLocal
import wolframalpha
#from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

print("Initializing Airi")

MASTER = "Arpit"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# speak function will speak the string rather pronounce the string whcih is passsed to it
def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning " + MASTER)

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening")

    speak("I am Airi. How may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Say that again please")
        query = None
    return query


def takeCommandINT():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening...")
        audio = r.listen(source)

    try:
        # print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
        query = int(query)

    except Exception as e:
        print("Say that again please")
        query = None
        takeCommand()
    return query


# def sendemail():
#  server = smtplib.SMTP('smtp.gmail.com', 587)
#  server.ehlo()
#  server.starttls()
#  server.login('arpit.music19@gmail.com', 'mujhenahipata')
#  server.sendmail("arpit.mohapatra19@gmail.com", to, content)
#  server.close()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


service = authenticate_google()
get_events(2, service)

# main function starts here ....



def main():
    # basic tasks

    speak("Initializing Airi.....")
    wishMe()
    query = takeCommand()

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


    if 'wikipedia' in query.lower():
        speak('Searching wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=4)
        print(results)
        speak(results)

    elif 'open youtube' in query.lower():
        url = "youtube.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open google' in query.lower():
        url = "google.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open instagram' in query.lower():
        url = "instagram.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'play music' or 'play some music' or 'play BTS' in query.lower():
        songs_dir = "C:\\Users\\KIIT\\Desktop\\music\\BTS"
        songs = os.listdir(songs_dir)
        if 'play' in query.lower():
            speak(f"Which track number {MASTER}")
            q2 = takeCommandINT()
        print(songs[q2])
        os.startfile(os.path.join(songs_dir, songs[q2]))

    elif 'time' in query.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{MASTER} the time is {strTime}")

    elif 'open pycharm' in query.lower():
        codePath = "C:\Program Files\JetBrains\PyCharm Community Edition 2019.3.1"
        os.startfile(codePath)

    # elif 'open spotify' in query.lower():
      #  codePath = "C:\\Users\\KIIT\\Desktop\\Spotify"
      #  os.startfile(codePath)

main()