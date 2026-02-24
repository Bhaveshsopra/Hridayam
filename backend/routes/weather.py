"""Weather API routes."""

from flask import Blueprint, request, jsonify
from services.weather_services import WeatherService
from config import Config

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    """Get weather for a city in MP."""
    weather = WeatherService.get_weather(
        city, api_key=Config.WEATHER_API_KEY
    )

    return jsonify({
        "success": True,
        "weather": weather,
    })


@weather_bp.route("/weather", methods=["GET"])
def get_all_weather():
    """Get weather for major MP cities."""
    cities = [
        "Bhopal", "Indore", "Gwalior", "Ujjain",
        "Jabalpur", "Khajuraho", "Pachmarhi",
    ]
    results = {}

    for city in cities:
        results[city] = WeatherService.get_weather(
            city, api_key=Config.WEATHER_API_KEY
        )

    return jsonify({
        "success": True,
        "weather": results,
    })