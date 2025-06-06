from email.mime import audio

import speech_recognition as sr
import os
import webbrowser
import openai
import datetime as dt

import win32com.client as win32
speaker = win32.Dispatch("SAPI.SpVoice")

def say(text):
    speaker.Speak(text)
    print(f"SAM : {text}")

def voice():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            query = r.recognize_google(audio,language='en-in')
            print("User Said :",query)
            return query
        except Exception as e:
            return "Say that again please..."




if __name__=="__main__":
    print("Hello I am SAM A,I")
    say("HELLO I am SAM A,I")
    while True:
        print("Listening...")
        text= voice()
        apps=[["Spotify","C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe"]]
        sites=[["Youtube","https://www.youtube.com/"],["Google","https://www.google.com/"],["Wikipedia","https://www.wikipedia.org/"]]
        #To Open Sites....
        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                webbrowser.open(site[1])
                say(f"Openning {site[0]} Sir....")

        #To Open Apps...
        for app in apps:
            if f"Open {app[0]}".lower() in text.lower():
                os.startfile(app[1])
                say(f"Opening {app[0]} Sir....")

        #To Tell Date and Time
        if "The time".lower() in text.lower():
            time=dt.datetime.now().strftime("%H:%M")
            say(f"Sir the time is {time}")

        if "Date".lower() in text.lower():
            time=dt.datetime.now().date().strftime("%d-%m-%Y")
            say(f"Sir the Date is {time}")
        say(text)







