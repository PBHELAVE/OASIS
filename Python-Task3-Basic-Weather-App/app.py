import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Python Weather App")
st.write("Get current weather information for any city.")

city = st.text_input(
    "Enter city name",
    placeholder="e.g. Nagpur"
)

if st.button("🔍 Get Weather"):

    if not city.strip():

        st.warning("Please enter a city name.")

    elif not API_KEY:

        st.error(
            "OpenWeather API key is missing. "
            "Please check your .env file."
        )

    else:

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city.strip(),
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

                st.success(
                    f"Weather found for {city_name}, {country}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{temperature:.1f} °C"
                    )

                with col2:
                    st.metric(
                        "🌡️ Feels Like",
                        f"{feels_like:.1f} °C"
                    )

                st.write(
                    f"### ☁️ {condition.title()}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.info(
                        f"💧 Humidity: {humidity}%"
                    )

                with col2:
                    st.info(
                        f"💨 Wind Speed: {wind_speed} m/s"
                    )

            elif response.status_code == 404:

                st.error(
                    f"City '{city}' was not found."
                )

            elif response.status_code == 401:

                st.error(
                    "Invalid or inactive OpenWeather API key."
                )

            else:

                st.error(
                    f"Weather service error: "
                    f"{response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Internet connection error. "
                "Please check your internet connection."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Weather service timed out. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"❌ Request error: {error}"
            )

        except Exception:

            st.error(
                "Something went wrong. "
                "Please try again."
            )
            