# Python Basic Weather App

A Python-based Basic Weather Application developed as part of the OIBSIP Python Programming Internship – Task 3.

The application uses the OpenWeather API to fetch real-time weather information for a city entered by the user. It provides weather details such as temperature, feels-like temperature, weather condition, humidity, and wind speed.

# Author

Payal Bhelave

Python Programming Internship  
OIBSIP – Task 3

# Project Description

This project demonstrates how Python can be used to build a simple weather application using an external REST API.

The application:

-Accepts a city name from the user.
-Connects to the OpenWeather API.
-Fetches real-time weather information.
-Processes the JSON response.
-Displays weather details in a simple and user-friendly interface.
-Handles invalid cities and API/network errors.
-Uses environment variables to securely store the API key.

The project was later enhanced with a Streamlit-based graphical web interface for a better user experience.

# Features

🔹 Basic Features

City name input  
Real-time weather information  
Temperature display  
Feels-like temperature  
Weather condition  
Humidity information  
Wind speed information  
OpenWeather API integration  
JSON data processing  

🔹 Advanced Features

Streamlit web interface  
API key management using `.env`  
Invalid city handling  
Missing API key handling  
Invalid API key handling  
Internet connection error handling  
Request timeout handling  
User-friendly error messages  
Responsive weather information display  

# Technologies Used

Python : Core programming language  
Streamlit : Web application interface  
Requests : API requests  
OpenWeather API : Real-time weather information  
python-dotenv : Environment variable management  
JSON : API response data processing  

# Project Structure

Python-Task3-Basic-Weather-App/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
│
└── screenshots/
    ├── 01_home.png
    ├── 02_nagpur_weather.png
    ├── 03_mumbai_weather.png
    ├── 04_invalid_city.png
    └── 05_error_handling.png

# How It Works

1.The user opens the Weather App.
2.The user enters a city name.
3.The application validates the input.
4.The application sends a request to the OpenWeather API.
5.The API returns weather information in JSON format.
6.The application extracts the required weather details.
7.The weather information is displayed to the user.

# Weather Information Displayed

The application displays:

-City and country
-Current temperature
-Feels-like temperature
-Weather condition
-Humidity
-Wind speed

# Error Handling

The application handles common errors such as:

-Empty city name
-Invalid city name
-City not found
-Missing OpenWeather API key
-Invalid API key
-Internet connection failure
-Request timeout
-API request errors

Instead of displaying Python errors or crashing, the application displays user-friendly error messages.


# Running the Application

Run the Streamlit application using:

    streamlit run app.py

The application will open in the browser.

# Example

Enter:

    Nagpur

The application displays the current weather information for Nagpur.

Other cities that can be tested:

-mumbai
-akola
-Pune
-Hyderabad
-Bangalore
-Chennai

# Learning Outcomes

Through this project, I learned:

-Python API integration
-Working with REST APIs
-Processing JSON data
-Using environment variables
-API error handling
-Exception handling
-Streamlit application development
-Building a simple Python web application
-Creating user-friendly interfaces

