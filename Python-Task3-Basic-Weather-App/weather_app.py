import os
import requests
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    if not API_KEY:
        print("Error: OpenWeather API key is missing.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            city_name = data["name"]
            country = data["sys"]["country"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]

            print("\n" + "=" * 45)
            print("       WEATHER INFORMATION")
            print("=" * 45)

            print(f"City        : {city_name}, {country}")
            print(f"Temperature : {temperature:.1f} °C")
            print(f"Feels Like  : {feels_like:.1f} °C")
            print(f"Condition   : {condition}")
            print(f"Humidity    : {humidity}%")
            print(f"Wind Speed  : {wind_speed} m/s")

            print("=" * 45)

        elif response.status_code == 404:

            print(f"City '{city}' was not found.")
            print("Please check the city name.")

        elif response.status_code == 401:

            print("Invalid or inactive API key.")

        else:

            print(
                "Unable to fetch weather information."
            )

    except requests.exceptions.ConnectionError:

        print("Internet connection error.")

    except requests.exceptions.Timeout:

        print("Weather service timed out.")

    except requests.exceptions.RequestException as error:

        print("Request error:", error)


def main():

    print("=" * 45)
    print("         PYTHON WEATHER APP")
    print("=" * 45)

    city = input("\nEnter city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    get_weather(city)

    print("\nThank you for using the Weather App!")


if __name__ == "__main__":
    main()