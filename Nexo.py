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

# Decode API Key for OpenAI 
api_key = base64.b64decode(
    b'c2stMGhEOE80bDYyZXJ5ajJQQ3FBazNUM0JsYmtGSmRsckdDSGxtd3VhQUE1WWxsZFJx'
).decode("utf-8")
openai.api_key = api_key

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def send_email(to, content):
    """Send an email via SMTP."""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()

def speak_news():
    """Fetch and speak top news headlines."""
    url = "http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=yourapikey"
    news = requests.get(url).json()
    speak("Source: The Times Of India. Today's Headlines are..")
    for index, article in enumerate(news.get("articles", [])):
        speak(article.get("title", "No title available"))
        if index == 4:  # Read only the first 5 headlines
            break
    speak("These were the top headlines. Have a great day∂!")


def ask_gpt3(question):
    """Ask Fine-tuned GPT a question and get a response."""
    response = openai.Completion.create(
        model="ft:gpt-3.5-turbo-0125:personal::AU5skETV", prompt=f"Answer: {question}\n", max_tokens=150, temperature=0.7
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
