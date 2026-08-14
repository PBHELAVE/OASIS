# Python Voice Assistant

A Python-based Voice Assistant developed as part of the OIBSIP Python Programming Internship – Task 1.

The assistant uses Speech Recognition to understand voice commands and Text-to-Speech (TTS) to respond audibly. It can perform everyday tasks such as telling the time and date, searching the web, fetching weather information, setting reminders, answering general-knowledge questions, opening custom websites, and sending emails.


# Author

Payal Bhelave

Python Programming Internship  
OIBSIP – Task 1


# Project Description

This project demonstrates how Python can be used to build an interactive voice-controlled assistant.

The assistant:

-Listens to the user's voice through a microphone.
-Converts speech into text.
-Identifies the user's intention.
-Performs the requested task.
-Converts the response back into speech.

The project also includes advanced features such as weather API integration, timed reminders, general knowledge retrieval, custom commands, and email functionality.


# Features

🔹 Basic Features

Speech recognition
Text-to-speech responses
Greeting system
Current time
Current date
Web search
Error handling
Natural-language command detection

🔹 Advanced Features

Weather information
Timed reminders
General knowledge using Wikipedia
Custom voice commands
Email sending through SMTP
Environment-variable based API credentials


# Technologies Used


Python : Core programming language 
SpeechRecognition : Speech-to-text 
PyAudio : Microphone input 
pyttsx3 : Text-to-speech 
Requests : API requests 
OpenWeather API : Weather information 
Wikipedia API : General knowledge 
smtplib : Email functionality 
python-dotenv : Environment variables 
threading : Background reminders 
webbrowser : Opening websites 
JSON : Custom command configuration 


# Project Structure

```text
Python-Task1-Voice-Assistant/
│
├── .env
├── .gitignore
├── custom_commands.json
├── README.md
├── requirements.txt  
├── voice_assistant.py
│
└── screenshots/
    ├── 01_starting.png
    ├── 02_greeting.png
    ├── 03_time.png
    ├── 04_date.png
    ├── 05_search.png
    ├── 06_weather.png
    ├── 07_reminder.png
    ├── 08_generalknowledge.png
    ├── 09_customcommands.png
    └── 10_email.png