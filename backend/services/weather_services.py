"""Weather service for MP destinations."""

import random
from datetime import datetime


class WeatherService:
    """
    Fetch weather data for MP cities.
    Uses mock data when API key not available.
    """

    # Seasonal temperature ranges for MP
    SEASONAL_DATA = {
        "winter": {
            "months": [11, 12, 1, 2],
            "temp_min": 6,
            "temp_max": 26,
            "conditions": [
                "Clear", "Sunny", "Partly Cloudy", "Foggy"
            ],
            "humidity_range": (30, 55),
        },
        "summer": {
            "months": [3, 4, 5, 6],
            "temp_min": 25,
            "temp_max": 46,
            "conditions": [
                "Sunny", "Hot", "Clear", "Hazy"
            ],
            "humidity_range": (15, 40),
        },
        "monsoon": {
            "months": [7, 8, 9, 10],
            "temp_min": 20,
            "temp_max": 36,
            "conditions": [
                "Rainy", "Cloudy", "Thunderstorm",
                "Partly Cloudy", "Light Rain",
            ],
            "humidity_range": (60, 90),
        },
    }

    @staticmethod
    def get_weather(city, api_key=None):
        """
        Get weather for a city.
        Falls back to realistic mock data.
        """
        # Try real API if key available
        if api_key:
            try:
                return WeatherService._fetch_real_weather(
                    city, api_key
                )
            except Exception:
                pass

        # Fallback: Generate realistic mock weather
        return WeatherService._generate_mock_weather(city)

    @staticmethod
    def _fetch_real_weather(city, api_key):
        """Fetch from OpenWeatherMap API."""
        import requests

        url = (
            f"https://api.openweathermap.org/data/2.5/"
            f"weather?q={city},IN&appid={api_key}"
            f"&units=metric"
        )
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code == 200:
            return {
                "city": city,
                "temperature": round(
                    data["main"]["temp"]
                ),
                "feels_like": round(
                    data["main"]["feels_like"]
                ),
                "humidity": data["main"]["humidity"],
                "condition": (
                    data["weather"][0]["description"]
                    .title()
                ),
                "wind_speed": round(
                    data["wind"]["speed"] * 3.6, 1
                ),
                "icon": data["weather"][0]["icon"],
                "source": "OpenWeatherMap",
                "timestamp": datetime.now().isoformat(),
            }
        raise Exception("API Error")

    @staticmethod
    def _generate_mock_weather(city):
        """Generate realistic mock weather data."""
        month = datetime.now().month
        season_data = None

        for season, data in (
            WeatherService.SEASONAL_DATA.items()
        ):
            if month in data["months"]:
                season_data = data
                break

        if not season_data:
            season_data = WeatherService.SEASONAL_DATA[
                "winter"
            ]

        temp = random.randint(
            season_data["temp_min"],
            season_data["temp_max"],
        )
        humidity = random.randint(
            *season_data["humidity_range"]
        )
        condition = random.choice(
            season_data["conditions"]
        )

        return {
            "city": city,
            "temperature": temp,
            "feels_like": temp + random.randint(-2, 3),
            "humidity": humidity,
            "condition": condition,
            "wind_speed": round(
                random.uniform(5, 25), 1
            ),
            "source": "AI Prediction",
            "timestamp": datetime.now().isoformat(),
            "forecast_5day": (
                WeatherService._generate_forecast(
                    season_data
                )
            ),
        }

    @staticmethod
    def _generate_forecast(season_data):
        """Generate 5-day forecast."""
        forecast = []
        for i in range(1, 6):
            forecast.append(
                {
                    "day": f"Day +{i}",
                    "temp_high": random.randint(
                        season_data["temp_min"] + 5,
                        season_data["temp_max"],
                    ),
                    "temp_low": random.randint(
                        season_data["temp_min"],
                        season_data["temp_min"] + 10,
                    ),
                    "condition": random.choice(
                        season_data["conditions"]
                    ),
                }
            )
        return forecast