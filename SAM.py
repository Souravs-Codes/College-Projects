import os
import speech_recognition as sr
import webbrowser
import datetime as dt
from huggingface_hub import InferenceClient
import win32com.client as win32

# Text-to-speech setup
speaker = win32.Dispatch("SAPI.SpVoice")

def say(text):
    print(f"SAM: {text}")
    speaker.Speak(text)


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
    token = os.getenv("HF_TOKEN")
    if not token:
        return "❌ Hugging Face token not set in environment."

    client = InferenceClient(token=token)

    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI error: {e}"

# Main assistant loop
if __name__ == "__main__":
    say("Hello, I am SAM A.I.")

    apps = [["Spotify", "C:\\Users\\win11\\AppData\\Roaming\\Spotify\\Spotify.exe"]]
    sites = [
        ["Youtube", "https://www.youtube.com/"],
        ["Google", "https://www.google.com/"],
        ["Wikipedia", "https://www.wikipedia.org/"]
    ]

    while True:
        text = voice().lower()

        # Open websites
        for site in sites:
            if f"open {site[0].lower()}" in text:
                webbrowser.open(site[1])
                say(f"Opening {site[0]} sir...")
                break

        # Open applications
        for app in apps:
            if f"open {app[0].lower()}" in text:
                os.startfile(app[1])
                say(f"Opening {app[0]} sir...")
                break

        # Report time
        if "the time" in text:
            current_time = dt.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {current_time}")

        # Report date
        elif "date" in text:
            current_date = dt.datetime.now().strftime("%d-%m-%Y")
            say(f"Sir, the date is {current_date}")

        # Ask AI
        elif "SAM tell me" in text or "question" in text or "what is" in text:
            say("Yes sir??")
            user_prompt = voice()
            ai_response = ai(user_prompt)
            say(ai_response)
