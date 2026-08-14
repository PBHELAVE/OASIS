import os
import re
import json
import time
import threading
import webbrowser
import smtplib
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import quote_plus

import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# =========================================================
# CONFIGURATION
# =========================================================
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Custom commands file
CUSTOM_COMMANDS_FILE = os.path.join(
    BASE_DIR,
    "custom_commands.json"
)

# Prevent microphone from listening while reminder speaks
reminder_active = False


# =========================================================
# TEXT TO SPEECH
# =========================================================

import pyttsx3
import threading

tts_lock = threading.Lock()


def speak(text):
    """Reliable Windows text-to-speech."""

    if not text:
        return

    print("Assistant:", text)

    try:
        with tts_lock:

            # Create a fresh engine for every response
            speech_engine = pyttsx3.init("sapi5")

            speech_engine.setProperty(
                "rate",
                165
            )

            speech_engine.setProperty(
                "volume",
                1.0
            )

            voices = speech_engine.getProperty(
                "voices"
            )

            if voices:
                speech_engine.setProperty(
                    "voice",
                    voices[0].id
                )

            speech_engine.say(
                str(text)
            )

            speech_engine.runAndWait()

            speech_engine.stop()

            del speech_engine

    except Exception as error:

        print(
            "TTS ERROR:",
            repr(error)
        )

# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()


def listen(timeout=5, phrase_time_limit=8):
    """Listen to microphone and return recognized text."""

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            try:

                audio = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            except sr.WaitTimeoutError:

                print("No speech detected.")

                return ""

        print("Recognizing...")

        text = recognizer.recognize_google(
            audio
        )

        text = text.lower().strip()

        print("You:", text)

        return text

    except sr.UnknownValueError:

        speak(
            "Sorry, I could not understand you. "
            "Please repeat."
        )

        return ""

    except sr.RequestError as error:

        print("Speech recognition error:", error)

        speak(
            "Speech recognition service is unavailable."
        )

        return ""

    except Exception as error:

        print("Microphone error:", error)

        speak(
            "I could not access the microphone."
        )

        return ""


# =========================================================
# GREETING
# =========================================================

def greeting():

    hour = datetime.now().hour

    if hour < 12:
        speak("Good morning!")

    elif hour < 18:
        speak("Good afternoon!")

    else:
        speak("Good evening!")

    speak(
        "Hello! How can I help you?"
    )


# =========================================================
# TIME
# =========================================================

def tell_time():

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"The current time is {current_time}."
    )


# =========================================================
# DATE
# =========================================================

def tell_date():

    current_date = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        f"Today is {current_date}."
    )


# =========================================================
# WEB SEARCH
# =========================================================

def search_web(command):

    search_text = command.strip()

    prefixes = [
        "search for ",
        "search ",
        "look up "
    ]

    for prefix in prefixes:

        if search_text.startswith(prefix):

            search_text = search_text[
                len(prefix):
            ].strip()

            break

    if not search_text:

        speak(
            "What would you like me to search for?"
        )

        search_text = listen()

    if not search_text:
        return

    url = (
        "https://www.google.com/search?q="
        + quote_plus(search_text)
    )

    try:

        webbrowser.open(url)

        speak(
            f"I opened a search for {search_text}."
        )

    except Exception as error:

        print("Browser error:", error)

        speak(
            "I could not open the web browser."
        )


# =========================================================
# WEATHER
# =========================================================

def clean_city_name(text):

    city = text.lower().strip()

    patterns = [
        r"what is the weather in ",
        r"what's the weather in ",
        r"what is today's weather in ",
        r"today's weather in ",
        r"todays weather in ",
        r"weather in ",
        r"weather for ",
        r"temperature in ",
        r"temperature for ",
        r"forecast for "
    ]

    for pattern in patterns:

        city = re.sub(
            pattern,
            "",
            city,
            flags=re.IGNORECASE
        )

    city = re.sub(
        r"\s+weather$",
        "",
        city,
        flags=re.IGNORECASE
    )

    city = city.replace("'s", "")

    return city.strip()


def get_weather(city):

    if not city:

        speak(
            "I could not understand the city."
        )

        return False

    if not OPENWEATHER_API_KEY:

        speak(
            "The weather API key is missing."
        )

        return False

    print(
        f"Fetching weather for: {city}"
    )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        print(
            "Weather API status:",
            response.status_code
        )

        if response.status_code == 200:

            data = response.json()

            main_data = data.get(
                "main",
                {}
            )

            weather_data = data.get(
                "weather",
                [{}]
            )[0]

            wind_data = data.get(
                "wind",
                {}
            )

            temperature = main_data.get(
                "temp"
            )

            feels_like = main_data.get(
                "feels_like"
            )

            humidity = main_data.get(
                "humidity"
            )

            condition = weather_data.get(
                "description",
                "unknown"
            )

            wind_speed = wind_data.get(
                "speed",
                0
            )

            message = (
                f"The weather in {city} is "
                f"{condition}. "
                f"The temperature is "
                f"{temperature:.1f} degrees Celsius. "
                f"It feels like "
                f"{feels_like:.1f} degrees. "
                f"Humidity is {humidity} percent. "
                f"Wind speed is "
                f"{wind_speed} meters per second."
            )

            speak(message)

            return True

        elif response.status_code == 404:

            speak(
                f"I could not find the city {city}."
            )

            return False

        elif response.status_code == 401:

            speak(
                "The weather API key is invalid "
                "or not active."
            )

            return False

        else:

            print(
                "Weather response:",
                response.text
            )

            speak(
                "I could not fetch the weather."
            )

            return False

    except requests.exceptions.RequestException as error:

        print(
            "Weather connection error:",
            error
        )

        speak(
            "I could not connect to the weather service."
        )

        return False


def weather_command(command=None):

    # Example:
    # "what is the weather in Nagpur"

    if command:

        city = clean_city_name(command)

        if city and city not in [
            "today's",
            "todays"
        ]:

            if get_weather(city):
                return

    # Ask user for city

    speak(
        "Which city would you like "
        "the weather for?"
    )

    city = listen()

    if not city:

        speak(
            "I could not understand the city name."
        )

        return

    city = clean_city_name(city)

    get_weather(city)


# =========================================================
# REMINDER
# =========================================================

def reminder_worker(seconds, message):

    global reminder_active

    reminder_active = True

    print(
        f"Reminder timer started for "
        f"{seconds} seconds."
    )

    time.sleep(seconds)

    print("REMINDER TRIGGERED")

    speak(
        f"Reminder: {message}"
    )

    # Prevent microphone from hearing
    # the assistant's own voice.
    time.sleep(1)

    reminder_active = False


def extract_seconds(text):

    numbers = re.findall(
        r"\d+",
        text
    )

    if not numbers:
        return None

    return int(numbers[0])


def set_reminder(command=None):

    global reminder_active

    try:

        # -------------------------------------------------
        # ONE-LINE REMINDER
        # -------------------------------------------------

        if command:

            match = re.search(
                r"remind me in "
                r"(\d+)\s*"
                r"(second|seconds|minute|minutes)"
                r"(?:\s+to)?\s+(.+)",
                command
            )

            if match:

                number = int(
                    match.group(1)
                )

                unit = match.group(2)

                message = match.group(3).strip()

                if "minute" in unit:

                    seconds = number * 60

                else:

                    seconds = number

                if seconds <= 0:

                    speak(
                        "Please provide a valid time."
                    )

                    return

                speak(
                    f"Okay, I will remind you "
                    f"in {number} {unit}."
                )

                threading.Thread(
                    target=reminder_worker,
                    args=(
                        seconds,
                        message
                    ),
                    daemon=True
                ).start()

                return

        # -------------------------------------------------
        # TWO-STEP REMINDER
        # -------------------------------------------------

        speak(
            "What should I remind you about?"
        )

        message = listen()

        if not message:

            speak(
                "I could not understand "
                "the reminder."
            )

            return

        speak(
            "In how many seconds should "
            "I remind you?"
        )

        duration_text = listen(
            timeout=10,
            phrase_time_limit=5
        )

        if not duration_text:

            speak(
                "I could not understand "
                "the time."
            )

            return

        print(
            "Reminder duration received:",
            duration_text
        )

        seconds = extract_seconds(
            duration_text
        )

        if seconds is None:

            speak(
                "Please say a number of seconds."
            )

            return

        if seconds <= 0:

            speak(
                "Please provide a number "
                "greater than zero."
            )

            return

        speak(
            f"Okay, I will remind you "
            f"in {seconds} seconds."
        )

        threading.Thread(
            target=reminder_worker,
            args=(
                seconds,
                message
            ),
            daemon=True
        ).start()

    except Exception as error:

        print(
            "Reminder error:",
            error
        )

        speak(
            "There is a problem "
            "with the reminder."
        )

        reminder_active = False


# =========================================================
# GENERAL KNOWLEDGE
# =========================================================

def general_knowledge(command=None):

    if command:

        prefixes = [
            "who is ",
            "who was ",
            "what is ",
            "what was ",
            "tell me about ",
            "explain ",
            "about "
        ]

        question = command.strip()

        for prefix in prefixes:

            if question.startswith(prefix):

                question = question[
                    len(prefix):
                ].strip()

                break

    else:

        speak(
            "What would you like to know?"
        )

        question = listen()

    if not question:

        return

    # Wikipedia REST API

    url = (
        "https://en.wikipedia.org/api/rest_v1/"
        "page/summary/"
        + quote_plus(
            question.replace(" ", "_")
        )
    )

    headers = {
        "User-Agent":
        "PayalVoiceAssistant/1.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(
            "Wikipedia status:",
            response.status_code
        )

        if response.status_code == 200:

            data = response.json()

            answer = data.get(
                "extract"
            )

            if answer:

                # Keep speech short
                speak(
                    answer[:600]
                )

            else:

                speak(
                    "I could not find "
                    "information about that."
                )

        else:

            speak(
                "I could not find "
                "information about that."
            )

    except requests.exceptions.RequestException as error:

        print(
            "Knowledge API error:",
            error
        )

        speak(
            "I could not connect "
            "to the knowledge service."
        )


# =========================================================
# CUSTOM COMMANDS
# =========================================================

def load_custom_commands():

    print(
        "Looking for custom commands:"
    )

    print(
        CUSTOM_COMMANDS_FILE
    )

    if not os.path.exists(
        CUSTOM_COMMANDS_FILE
    ):

        print(
            "custom_commands.json not found."
        )

        return {}

    try:

        with open(
            CUSTOM_COMMANDS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            commands = json.load(file)

        print(
            "Custom commands loaded successfully."
        )

        return {
            key.lower().strip(): value
            for key, value in commands.items()
        }

    except json.JSONDecodeError as error:

        print(
            "Invalid custom_commands.json:",
            error
        )

        return {}

    except Exception as error:

        print(
            "Custom command error:",
            error
        )

        return {}


custom_commands = load_custom_commands()


def execute_custom_command(command):

    url = custom_commands.get(
        command
    )

    if not url:

        return False

    try:

        webbrowser.open(url)

        speak(
            f"Opening {command}."
        )

        return True

    except Exception as error:

        print(
            "Custom command error:",
            error
        )

        speak(
            "I could not open that website."
        )

        return False


# =========================================================
# EMAIL
# =========================================================

def send_email():

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:

        speak(
            "Email settings are missing."
        )

        return

    speak(
        "Who should I send the email to?"
    )

    recipient = listen()

    if not recipient:

        speak(
            "I could not understand "
            "the recipient."
        )

        return

    speak(
        "What should I write?"
    )

    body = listen(
        timeout=10,
        phrase_time_limit=20
    )

    if not body:

        speak(
            "I could not understand "
            "the email message."
        )

        return

    speak(
        "What should be the subject?"
    )

    subject = listen()

    if not subject:

        subject = "Voice Assistant Email"

    try:

        message = EmailMessage()

        message["From"] = EMAIL_ADDRESS

        message["To"] = recipient

        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            server.send_message(
                message
            )

        speak(
            "The email was sent successfully."
        )

    except Exception as error:

        print(
            "Email error:",
            error
        )

        speak(
            "I could not send the email."
        )


# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(command):

    command = command.lower().strip()

    # Exit FIRST

    if command in [
        "goodbye",
        "bye",
        "exit",
        "quit",
        "stop"
    ]:

        return "exit"

    # Custom command

    if command in custom_commands:

        return "custom"

    # Greeting

    if command in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "greeting"

    # Reminder

    if (
        "remind me" in command
        or "set a reminder" in command
        or command == "reminder"
    ):

        return "reminder"

    # Weather

    if (
        "weather" in command
        or "temperature" in command
        or "forecast" in command
    ):

        return "weather"

    # Email

    if (
        "send email" in command
        or "send an email" in command
    ):

        return "email"

    # Search

    if (
        command.startswith("search ")
        or command.startswith("search for ")
        or command.startswith("look up ")
    ):

        return "search"

    # Time

    if (
        command == "time"
        or "what time is it" in command
        or "what is the time" in command
        or "current time" in command
        or "tell me the time" in command
    ):

        return "time"

    # Date

    if (
        command == "date"
        or "today's date" in command
        or "todays date" in command
        or "what date is it" in command
        or "current date" in command
    ):

        return "date"

    # Knowledge

    if (
        command.startswith("who is ")
        or command.startswith("who was ")
        or command.startswith("what is ")
        or command.startswith("what was ")
        or command.startswith("tell me about ")
        or command.startswith("explain ")
        or command.startswith("about ")
    ):

        return "knowledge"

    return "unknown"


# =========================================================
# PROCESS COMMAND
# =========================================================

def process_command(command):

    print(
        "\nPROCESSING COMMAND:",
        command
    )

    command = command.lower().strip()

    intent = detect_intent(
        command
    )

    print(
        "DETECTED INTENT:",
        intent
    )

    if intent == "greeting":

        greeting()

    elif intent == "time":

        tell_time()

    elif intent == "date":

        tell_date()

    elif intent == "weather":

        weather_command(command)

    elif intent == "reminder":

        set_reminder(command)

    elif intent == "knowledge":

        general_knowledge(command)

    elif intent == "search":

        search_web(command)

    elif intent == "email":

        send_email()

    elif intent == "custom":

        execute_custom_command(command)

    elif intent == "exit":

        speak(
            "Goodbye! Have a nice day."
        )

        return False

    else:

        speak(
            "I don't understand "
            "that command yet."
        )

    return True


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=" * 50)
    print("PYTHON VOICE ASSISTANT")
    print("=" * 50)

    speak(
        "Voice assistant started."
    )

    running = True

    while running:

        try:

            # Do NOT listen while a reminder
            # is actively speaking/counting down.

            if reminder_active:

                time.sleep(0.2)

                continue

            command = listen()

            if command:

                running = process_command(
                    command
                )

        except KeyboardInterrupt:

            print(
                "\nAssistant stopped."
            )

            break

        except Exception as error:

            print(
                "Unexpected error:",
                error
            )

            speak(
                "Something went wrong. "
                "Please try again."
            )


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()