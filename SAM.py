import os
import urllib.parse
import speech_recognition as sr
import webbrowser
import datetime as dt
from huggingface_hub import InferenceClient
import win32com.client as win32
import pywhatkit as pw
import pyautogui as pg
import time


# Text-to-speech setup
speaker = win32.Dispatch("SAPI.SpVoice")
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else None

def say(text):
    print(f"SAM: {text}")
    speaker.Speak(text)


# Chat replies and basic conversation
def chat(text):
    token = os.getenv("HF_TOKEN")
    if not token or not client:
        error_msg = "❌ Hugging Face token not set or client not initialized."
        say(error_msg)
        return error_msg

    try:
        completion = client.chat.completions.create(
            model="EleutherAI/gpt-j-6b",
            messages=[{"role": "user", "content": text}],
        )
        response = completion.choices[0].message.content.strip()
        say(response)
        return response
    except Exception as e:
        error_msg = f"❌ AI error: {e}"
        say(error_msg)
        return error_msg

# Voice input from user
def voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print("User said:", query)
            return query
        except Exception as e:
            print("Speech recognition error:", e)
            return "Say that again please..."

# Hugging Face AI interaction
def ai(prompt: str) -> str:
    if not HF_TOKEN or not client:
        return "❌ Hugging Face token not set or client not initialized."

    try:
        completion = client.chat.completions.create(
            model="EleutherAI/gpt-j-6b",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI error: {e}"

#searching in youtube
def search_youtube(query):
    search = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={search}"
    webbrowser.open(url)

peoples=[["Kushan","8092876654"],["Me","7061973898"],["Papa","6205143357"],["Mummy","9132356424"],["Samrat","7004936302"],["Dadai","7004936302"],["Aryan","9142446712"]]
apps = [["Spotify", "C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe"],["File","shell:MyComputerFolder"],["Discord","C:\\Users\\win11\\Desktop\\Discord.lnk"]]
sites = [["Youtube", "https://www.youtube.com/"],["Google", "https://www.google.com/"],["Wikipedia", "https://www.wikipedia.org/"]]

# Main assistant loop
if __name__ == "__main__":
    say("Hello, I am SAM A.I.")

    while True:
        text = voice().lower()
        handled=False

        # Open websites
        for site in sites:
            if f"open {site[0].lower()}" in text:
                webbrowser.open(site[1])
                say(f"Opening {site[0]} sir...")
                handled = True
                break

        # Open applications
        for app in apps:
            running_apps={}
            if f"open {app[0].lower()}" in text:
                os.startfile(app[1])
                say(f"Opening {app[0]} sir...")
                handled = True
                break


        # Report time
        if "the time" in text:
            current_time = dt.datetime.now().strftime("%I:%M:%p")
            say(f"Sir, the time is {current_time}")
            handled = True
            continue

        # Report date
        elif "date" in text:
            current_date = dt.datetime.now().strftime("%d-%m-%Y")
            say(f"Sir, the date is {current_date}")
            handled = True
            continue

        elif "search in youtube" in text:
            say("What should I search on YouTube?")
            query = voice()
            say(f"Searching YouTube for {query}")
            search_youtube(query)
            handled = True

        elif "search google" in text:
            say("What should I search on Google?")
            query = voice()
            say(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            handled = True

        for person in peoples:
            if f"send message to {person[0].lower()}" in text:
                say("What message should I send Sir?")
                query = voice()

                os.system("start whatsapp:")  # On Windows

                time.sleep(3)  # wait for app to open

                pg.click(182, 151)
                pg.write(person[0])
                pg.click(324, 242)
                time.sleep(0.5)
                pg.press("enter")
                pg.click(324, 242)
                time.sleep(0.5)
                pg.write(query)
                pg.press("enter")


            #SPOTIFY CONTROLS________________________________________________________________________

        if "play music" in text:
            say("What should I play Sir?")
            query = voice().lower()
            if "Sammy" in query:
                os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
                time.sleep(5)
                pg.click(55, 251)
                time.sleep(2)
                pg.click(167, 484)

            if "mood changer" in query:
                os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
                time.sleep(5)
                pg.click(48, 343)
                time.sleep(2)
                pg.click(167, 484)

            if "bhajan" in query:
                os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
                time.sleep(5)
                pg.click(42, 506)
                time.sleep(2)
                pg.click(167, 484)


        #Shutting down
        if any(phrase in text for phrase in ["exit", "quit", "stop", "goodbye","rest"]):
            say("Shutting down sir. Goodbye.")
            break

