"""
NEXO is an advanced voice-controlled Windows assistant powered by a custom fine-tuned GPT model, offering seamless integration with system operations, third-party apps, and smart automation. 
It features voice-controlled application/web management, AI-powered Q&A, email automation, real-time news/weather updates, hardware control (mouse/keyboard), system monitoring, 
and multi-layer error handling with hybrid TTS/STT systems - all tailored for enhanced Windows productivity through natural language commands.

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
import threading
import time

import requests
import pyttsx3
import pyjokes
import speech_recognition as sr
import openai
import psutil
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


def on_press(key):
    
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ["1", "2", "left", "right"]:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print("Key pressed: " + k)
        return False  # stop listener; remove this if want more keys

def on_release(key):
    print("{0} release".format(key))
    if key == Key.esc():
        # Stop listener
        return False
    
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
    """Send email using SMTP protocol.
    
    Args:
        to (str): Recipient email address
        content (str): Email body content
    """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("youremail@gmail.com", "your-password")
    server.sendmail("youremail@gmail.com", to, content)
    server.close()

def ask_gpt3(question):
    """Query fine-tuned model for responses.
    
    Args:
        question (str): User's question/prompt
        
    Returns:
        str: AI-generated response
    """
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
    """Capture and process voice input using Google's speech recognition.
    
    Returns:
        str: Recognized text input
    """
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
    """Launch Windows applications based on voice command.
    
    Args:
        command (str): Name of application to open
    """
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
        "spotify": "Spotify.exe",
        "zoom": "Zoom.exe",
        "chrome": "chrome.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "outlook": "OUTLOOK.EXE",
        "teams": "Teams.exe",
        "whatsapp": "WhatsApp.exe"
    }
    if command in apps:
        subprocess.run(apps[command], shell=True)
    else:
        speak("Application not found in my list.")

def open_website(command):
    """Open web pages in default browser.
    
    Args:
        command (str): Name of website to open
    """
    sites = {
        "youtube": "https://www.youtube.com/",
        "google": "https://www.google.com/",
        "github": "https://github.com/NevilPatel01",
        "stackoverflow": "https://stackoverflow.com/",
        "linkedin": "https://www.linkedin.com/",
        "twitter": "https://twitter.com/",
        "facebook": "https://facebook.com/",
        "instagram": "https://instagram.com/",
        "wikipedia": "https://wikipedia.org/",
        "netflix": "https://netflix.com/",
        "amazon": "https://amazon.com/"
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

def get_weather(city_name):
    """Retrieve and announce weather information.
    
    Args:
        city_name (str): City for weather lookup
    """
    try:
        api_key = "your_openweather_api_key"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != 404:
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]
            speak(f"The temperature in {city_name} is {temperature}°C with {weather_desc}. Humidity is {humidity}%.")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Weather service unavailable. Check your internet connection.")

def set_reminder():
    """Create timed reminder based on user input."""
    speak("What should I remind you about?")
    message = take_command()
    if message == "none":
        return

    speak("In how many minutes?")
    time_input = take_command()
    try:
        minutes = int(''.join(filter(str.isdigit, time_input)))
        seconds = minutes * 60
        threading.Timer(seconds, lambda: speak(f"Reminder: {message}")).start()
        speak(f"Reminder set for {minutes} minutes.")
    except:
        speak("Invalid time format. Please try again.")

def play_music():
    """Play random music file from predefined directory."""
    try:
        songs = os.listdir(MUSIC_DIR)
        if songs:
            os.startfile(os.path.join(MUSIC_DIR, songs[0]))
        else:
            speak("No music files found.")
    except Exception as e:
        speak(f"Music playback error: {str(e)}")

def get_system_info():
    """Provide system status updates."""
    battery = psutil.sensors_battery()
    if battery:
        status = "plugged in" if battery.power_plugged else "not plugged in"
        speak(f"Battery is at {battery.percent}% and {status}.")
    else:
        speak("Battery information unavailable.")

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    speak(f"Current CPU usage is {cpu_usage}% and memory usage is {memory_usage}%.")

def show_help():
    """Display available commands in console."""
    help_text = """
    Available Commands:
    - Open [application]: Launch installed programs
    - Website [name]: Open common websites
    - News: Current headlines
    - Screenshot: Capture screen
    - Joke: Tell a joke
    - Email: Send messages
    - Search for [query]: AI-powered search
    - Weather in [city]: Get weather updates
    - Set reminder: Create timed reminder
    - Play music: Audio playback
    - System info: Battery and performance
    - Help: Show this message
    - Exit: Close assistant
    """
    print(help_text)
    speak("Here are the available commands. Check console for details.")


def tell_joke():
    """Tell a random joke."""
    speak(pyjokes.get_joke())

def main():
    """Main program loop handling voice commands."""
    wish_user()
    while True:
        query = take_command()
        
        if not query or query == "none":
            continue
            
        if "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day.")
            break
            
        elif "open" in query:
            app_name = query.replace("open ", "").strip()
            open_application(app_name)
            
        elif "search for" in query:
            question = query.replace("search for", "").strip()
            speak(ask_gpt3(question))
            
        elif "news" in query:
            speak_news()
            
        elif "screenshot" in query:
            take_screenshot()
            
        elif "joke" in query:
            tell_joke()
            
        elif "email" in query:
            try:
                speak("What's the message content?")
                content = take_command()
                send_email("recipient@example.com", content)
            except Exception as e:
                speak(f"Email error: {str(e)}")
                
        elif "website" in query:
            site_name = query.replace("website", "").strip()
            open_website(site_name)
            
        elif "weather" in query:
            if "in" in query:
                city = query.split("in")[-1].strip()
            else:
                speak("Which city's weather?")
                city = take_command()
            if city != "none":
                get_weather(city)
                
        elif "reminder" in query:
            set_reminder()
            
        elif "play music" in query:
            play_music()
            
        elif "system" in query or "battery" in query:
            get_system_info()
            
        elif "help" in query:
            show_help()
            
        else:
            speak("I'm not sure how to help with that. Try 'help' for commands.")

if __name__ == "__main__":
    main()
