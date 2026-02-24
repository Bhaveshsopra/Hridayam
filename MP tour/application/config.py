import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "mp-tourism-ai-secret-2024")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///tourism.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenAI (optional - works without it too)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Weather API (free tier)
    WEATHER_API_KEY = os.getenv(
        "WEATHER_API_KEY", ""
    )

    # Mail settings (optional)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

    # SOS Emergency contacts
    EMERGENCY_CONTACTS = {
        "police": "100",
        "ambulance": "108",
        "women_helpline": "1091",
        "tourist_helpline": "1800-233-7777",
        "mp_tourism": "+91-755-2778383",
    }