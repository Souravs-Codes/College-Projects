import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import cv2
import threading
import os
import urllib.parse
import speech_recognition as sr
import webbrowser
import datetime as dt
import win32com.client as win32
import pywhatkit as pw
import pyautogui as pg
import time
from tkinter import scrolledtext
from serpapi import GoogleSearch
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


SERPAPI_KEY = "1596eee6d574a0e6a659fea634809a4d5296916880c36c7e6a3344a453d9ac67"
def google_search_summary(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    try:
        lines = []

        # Answer box info
        box = results.get("answer_box", {})
        if "snippet" in box:
            lines.append(box["snippet"])
        elif "answer" in box:
            lines.append(str(box["answer"]))
        elif "definition" in box:
            lines.append(box["definition"])
        elif "highlighted_snippet" in box:
            lines.append(box["highlighted_snippet"])

        # Organic snippets
        organic = results.get("organic_results", [])
        for res in organic[:2]:
            snippet = res.get("snippet")
            if snippet:
                lines.append(snippet)

        # Get the first organic result's link
        top_link = organic[0]['link'] if organic else None

        if lines:
            summary = " ".join(lines)
            return summary, top_link
        else:
            return "Sorry, I couldn't find detailed information.", None
    except Exception:
        return "Something went wrong while retrieving the search results.", None




# Text-to-speech setup
speaker = win32.Dispatch("SAPI.SpVoice")

def say(text):
    threading.Thread(target=speaker.Speak, args=(text,), daemon=True).start()

def say_blocking(text):
    speaker.Speak(text)

def long_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening (long)...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            query = r.recognize_google(audio, language='en-in')
            return query
        except sr.WaitTimeoutError:
            return "Listening timed out, please speak louder or faster."
        except Exception:
            return ""

def voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            return query
        except Exception:
            return "Say that again please..."


def search_youtube(query):
    search = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={search}"
    webbrowser.open(url)

peoples = [["Kushan", "8092876654"], ["Me".lower(), "7061973898"], ["Papa".lower(), "6205143357"], ["Mummy", "9132356424"], ["Samrat", "7004936302"], ["Dadai", "7004936302"], ["Aryan", "9142446712"]]
apps = [["Spotify", "C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe"], ["File", "shell:MyComputerFolder"], ["Discord", "C:\\Users\\win11\\Desktop\\Discord.lnk"]]
sites = [["Youtube", "https://www.youtube.com/"], ["Google", "https://www.google.com/"], ["Wikipedia", "https://www.wikipedia.org/"]]

def play_spotify_playlist(x, y):
    os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
    time.sleep(5)
    pg.click(x, y)
    time.sleep(1)
    pg.click(168, 472)
    time.sleep(0.5)
    pg.click(932, 1048)

def control_spotify_playlist(x, y):
    os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
    time.sleep(1)
    pg.click(x, y)
    time.sleep(0.5)
    pg.click(168, 472)
    time.sleep(0.5)
    pg.click(932, 1048)

class SAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAM - Simple AI Manager")
        self.root.geometry("900x600")
        self.root.configure(bg='black')


        # Background
        self.canvas = tk.Label(self.root, bg="black")
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Title label
        self.title_label = tk.Label(
            self.root,
            text="SAM - Simple AI Manager",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.root["bg"],
            highlightthickness=0,
            bd=0
        )

        self.title_label.place(relx=0.5, rely=0.05, anchor="n")
        self.title_label.lift()

        # Watermark
        self.watermark = tk.Label(
            self.root,
            text="Made By SAMMY",
            bg="black",  # solid background for visibility
            fg="white",
            font=("Arial", 8)
        )

        self.watermark.place(relx=0.957, rely=0.65, anchor="se", x=-5)
        self.watermark.lift()  # bring it above everything

        # Scrolled text area overlay
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 10),
            bg="black",
            fg="lime",
            height=8,
            bd=0,
            insertbackground="lime"
        )
        self.text_area.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.25)
        self.text_area.configure(state='disabled')

        self.cap = cv2.VideoCapture(resource_path("Particle.mp4"))

        self.running = True
        self.listening_thread = threading.Thread(target=self.listen_and_respond)
        self.listening_thread.start()

        self.root.after(1000, self.introduce_sam)
        self.root.after(10, self.update_video)

    def introduce_sam(self):
        self.show_text("🤖 SAM: Hello, I am SAM, your Simple AI Manager.")
        self.text_area.update_idletasks()

        say_blocking("Hello, I am SAM, your Simple AI Manager..")

        self.show_text("🔊 Started listening...")


        self.start_listening()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.canvas.configure(image=img)
            self.canvas.image = img
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.root.after(30, self.update_video)

    def start_listening(self):
        if not self.running:
            self.running = True
            self.listening_thread = threading.Thread(target=self.listen_and_respond)
            self.listening_thread.start()



    def listen_and_respond(self):
        while self.running:
            text = voice().lower()
            self.show_text(f"You: {text}")
            # You can implement custom response logic here
            for site in sites:
                if f"open {site[0].lower()}" in text:
                    webbrowser.open(site[1])
                    say(f"🤖 SAM: Opening {site[0]} sir...")
                    handled = True
                    break

            # Open applications
            for app in apps:
                running_apps = {}
                if f"open {app[0].lower()}" in text:
                    self.show_text(f"🤖 SAM: Opening {app[0]} sir...")
                    os.startfile(app[1])
                    say(f"Opening {app[0]} sir...")
                    handled = True
                    break

            # Report time
            if "the time" in text:
                current_time = dt.datetime.now().strftime("%I:%M:%p")
                self.show_text(f"🤖 SAM: Sir, the time is {current_time}")
                say(f"Sir, the time is {current_time}")
                handled = True
                continue

            # Report date
            elif "date" in text:
                current_date = dt.datetime.now().strftime("%d-%m-%Y")
                self.show_text(f"🤖 SAM: Sir, the date is {current_date}")
                say(f"Sir, the date is {current_date}")
                handled = True
                continue

            elif "search youtube" in text:
                self.show_text("🤖 SAM: What should I search on YouTube?")
                say("What should I search on YouTube?")
                query = long_voice().lower()
                self.show_text(f"🤖 SAM: Searching YouTube for {query}")
                say(f"Searching YouTube for {query}")
                search_youtube(query)
                handled = True





            elif "search google" in text:
                self.show_text("🤖 SAM: What should I search on Google?")
                say("What should I search on Google?")
                query = long_voice().lower()
                self.show_text(f"🤖 SAM: Searching Google for {query}")
                say(f"Searching Google for {query}")
                summary, top_link = google_search_summary(query)
                self.show_text(f"SAM: {summary}")
                say_blocking(summary)
                if top_link:
                    self.show_text("🤖 SAM: Should I open the webpage for this information?")
                    say("Should I open the webpage for this information? Please say yes or no.")
                    confirmation = long_voice().lower()
                    self.show_text(f"You: {confirmation}")
                    if "yes" in confirmation or "open" in confirmation:
                        self.show_text("🤖 SAM: Opening the page now.")
                        say("Opening the page now.")
                        webbrowser.open(top_link)
                    else:
                        self.show_text("🤖 SAM: Okay, not opening it.")
                        say("Okay, not opening it.")

            if "open the browser" in text:
                self.show_text("🤖 SAM: Opening the browser Sir...")
                say(f"Opening the browser Sir...")
                os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                handled = True

            if "close the browser" in text:
                os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                time.sleep(0.5)
                self.show_text("🤖 SAM: Closing the browser Sir...")
                say("Closing Browser Sir...")
                pg.hotkey('alt', 'f4')
                handled = True

            if "open whatsapp" in text:
                self.show_text("🤖 SAM: Opening whatsapp Sir...")
                say("Opening whatsapp Sir...")
                os.system("start whatsapp:")

            if "send message" in text:
                self.show_text("🤖 SAM: Who should I message Sir?")
                say(f"Who should I message Sir?")
                person=long_voice().lower()
                self.show_text("🤖 SAM: What message should I send Sir?")
                say("What message should I send Sir?")
                query = long_voice().lower()
                self.show_text(f"You: {query}")
                self.show_text(f"🤖 SAM: Sending Sir to {person}...")
                os.system("start whatsapp:")
                time.sleep(3)
                pg.click(182, 151)
                pg.write(person)
                pg.click(324, 242)
                time.sleep(0.5)
                pg.press("enter")
                pg.click(324, 242)
                time.sleep(0.5)
                pg.write(query)
                pg.press("enter")
                time.sleep(1)
                pg.click(1035, 1057)

            if any(phrase in text for phrase in ["close message", "close whatsapp"]):
                self.show_text(f"You: {text}")
                self.show_text("🤖 SAM: Closing whatsapp Sir...")
                say("Closing Whatsapp Sir...")
                os.system("start whatsapp:")
                time.sleep(0.5)
                pg.hotkey('alt', 'f4')
                handled = True

                # SPOTIFY CONTROLS________________________________________________________________________

            if "play music" in text:
                self.show_text(f"You: {text}")
                self.show_text("🤖 SAM: From which playlist should I play Sir?")
                say("From which playlist should I play Sir?")
                query = long_voice().lower()
                if "playlist" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Playing from Your Playlist Sir...")
                    say(f"Playing from Your Playlist Sir...")
                    play_spotify_playlist(54, 256)


                if "disco" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Playing from Mood Changer Playlist Sir...")
                    say(f"Playing from Mood Changer Playlist Sir...")
                    play_spotify_playlist(49, 422)

                if "bhajan" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Playing from  Bhajan Playlist Sir...")
                    say(f"Playing from Your Bhajan Playlist Sir...")
                    play_spotify_playlist(42, 506)

                if "bus" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Playing from Bus Driver Playlist Sir...")
                    say(f"Playing from Bus Driver Playlist Sir...")
                    play_spotify_playlist(58, 487)

            if "change the music" in text:

                self.show_text("🤖 SAM: Changing the Music Sir...")
                say(f"Changing the Music Sir...")
                pg.click(932, 1048)
                time.sleep(0.7)
                pg.hotkey('ctrl', 'right')
                time.sleep(0.2)
                pg.click(932, 1048)
                handled = True

            if any(phrase in text for phrase in ["pause", "stop"]):

                self.show_text("🤖 SAM: Pausing the Music Sir...")
                say(f"Pausing the Music Sir...")
                pg.click(932, 1048)
                time.sleep(0.7)
                pg.press('space')
                time.sleep(0.2)
                pg.click(932, 1048)
                handled = True

            if any(phrase in text for phrase in ["resume"]):

                self.show_text("🤖 SAM: Resuming the Music Sir...")
                say(f"Resuming the Music Sir...")
                pg.click(932, 1048)
                time.sleep(0.7)
                pg.press('space')
                time.sleep(0.2)
                pg.click(932, 1048)
                handled = True

            if "change to previous" in text:

                self.show_text("🤖 SAM: Changing to Previous Music Sir...")
                say(f"Changing to Previous Music Sir...")
                pg.click(932, 1048)
                time.sleep(0.7)
                pg.hotkey('ctrl', 'left')
                time.sleep(0.2)
                pg.click(932, 1048)
                handled = True

            if "change the playlist" in text:
                say("From which playlist should I play Sir?")
                query = long_voice().lower()
                if "playlist" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Changing Your Playlist Sir...")
                    say(f"Changing Your Playlist Sir...")
                    control_spotify_playlist(54, 256)

                if "disco" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Changing to Mood Changer Playlist Sir...")
                    say(f"Changing to Mood Changer Playlist Sir...")
                    control_spotify_playlist(49, 422)

                if "bhajan" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Changing Bhajan Playlist Sir...")
                    say(f"Changing Bhajan Playlist Sir...")
                    control_spotify_playlist(42, 506)

                if "bus" in query:
                    self.show_text(f"You: {text}")
                    self.show_text("🤖 SAM: Changing Bus Driver Playlist Sir...")
                    say(f"Changing Bus Driver Playlist Sir...")
                    control_spotify_playlist(58, 487)

            if any(phrase in text for phrase in ["close the Music", "close spotify"]):

                self.show_text("🤖 SAM: Closing Spotify Sir...")
                say(f"Closing Spotify Sir...")
                os.startfile("C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe")
                time.sleep(0.7)
                say("Closing Spotify Sir...")
                pg.hotkey('alt', 'f4')
                handled = True

            if any(phrase in text for phrase in ["exit", "quit", "goodbye", "rest", "shut down", "shutdown"]):

                self.show_text("🤖 SAM: Shutting Down Sir, Goodbye...")
                say("Shutting down sir, Goodbye.")
                self.running = False  # stop listening loop
                self.root.after(3000, self.root.destroy)  # close app after 1 sec (to allow speech)
                break

    def respond(self, text):
        self.show_text(f"🤖 SAM: {text}")
        say(text)

    def show_text(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SAMApp(root)
    root.mainloop()
