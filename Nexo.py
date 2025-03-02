"""
NEXO Voice Assistant: Control Windows programs with your voice
Author: Nevil Patel
Version: v0.1
"""

# Import necessary modules
import datetime
import subprocess
import webbrowser
import smtplib
import json
import os
import base64
import requests
import pyttsx3
import pyjokes
import speech_recognition as sr
import openai
from PIL import ImageGrab
from gtts import gTTS
from playsound import playsound
from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("voice", engine.getProperty("voices")[0].id)
engine.setProperty("rate", 150)

# Decode API Key for OpenAI (Replace with your API key securely)
api_key = base64.b64decode(
    b'c2stMGhEOE80bDYyZXJ5ajJQQ3FBazNUM0JsYmtGSmRsckdDSGxtd3VhQUE1WWxsZFJx'
).decode("utf-8")
openai.api_key = api_key

# Configuration constants
MUSIC_DIR = "C:\\Music"  # Update with your music directory
SCREENSHOT_DIR = "C:\\Screenshots"  # Update with preferred screenshot location



def speak(text):
    """Convert text to speech using pyttsx3 engine.
    
    Args:
        text (str): Text to be spoken aloud
    """
    engine.say(text)
    engine.runAndWait()


def speak_news():
    """Fetch and speak top news headlines."""
    url = "http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=yourapikey"
    news = requests.get(url).json()
    speak("Source: The Times Of India. Today's Headlines are..")
    for index, article in enumerate(news.get("articles", [])):
        speak(article.get("title", "No title available"))
        if index == 4:  # Read only the first 5 headlines
            break
    speak("These were the top headlines. Have a great day!")

def send_email(to, content):
    """Send an email via SMTP."""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()

def ask_gpt3(question):
    """Ask OpenAI's GPT-3 a question and get a response."""
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=f"Answer: {question}\n", max_tokens=150, temperature=0.7
    )
    return response.choices[0].text.strip()

def wish_user():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Nexo! How can I assist you?")

def take_command():
    """Capture and recognize speech input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio, language="en-in")
    except Exception:
        speak("I didn't catch that. Could you repeat?")
        return "None"

def open_application(command):
    """Open applications based on voice command."""
    apps = {
        "notepad": "Notepad.exe",
        "calculator": "calc.exe",
        "sticky notes": "StikyNot.exe",
        "powershell": "powershell.exe",
        "paint": "mspaint.exe",
        "command prompt": "cmd.exe",
        "discord": "discord.exe",
        "vscode": "code",
        "docker": "docker desktop",
        "task manager": "taskmgr.exe",
        "file explorer": "explorer.exe",
    }
    if command in apps:
        subprocess.run(apps[command], shell=True)
    else:
        speak("Application not found in my list.")

def open_website(command):
    """Open common websites based on voice command."""
    sites = {
        "youtube": "https://www.youtube.com/",
        "google": "https://www.google.com/",
        "github": "https://github.com/NevilPatel01",
        "stackoverflow": "https://stackoverflow.com/",
        "linkedin": "https://www.linkedin.com/",
    }
    if command in sites:
        webbrowser.open(sites[command])
    else:
        speak("Website not available in my list.")

def take_screenshot():
    """Enhanced screenshot capture with directory creation"""
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        filename = f"{SCREENSHOT_DIR}\\screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        ImageGrab.grab().save(filename)
        speak("Screenshot captured successfully")
    except Exception as e:
        speak(f"Screenshot failed: {str(e)}")

def tell_joke():
    """Tell a random joke."""
    speak(pyjokes.get_joke())

def main():
    """Main loop to process voice commands."""
    wish_user()
    while True:
        query = take_command().lower()
        if query == "exit" or query == "quit":
            speak("Goodbye! Have a great day.")
            break
        elif "open" in query:
            app_name = query.replace("open ", "")
            open_application(app_name)
        elif "search for" in query:
            question = query.replace("search for", "")
            answer = ask_gpt3(question)
            speak(answer)
        elif "news" in query:
            speak_news()
        elif "screenshot" in query:
            take_screenshot()
        elif "joke" in query:
            tell_joke()
        elif "email" in query:
            try:
                speak("What should I say?")
                content = take_command()
                send_email("recipient@example.com", content)
                speak("Email has been sent!")
            except:
                speak("Sorry, I couldn't send the email.")
        elif "website" in query:
            site_name = query.replace("website ", "")
            open_website(site_name)
        else:
            speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    main()
