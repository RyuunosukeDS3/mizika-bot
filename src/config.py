import os
from dotenv import load_dotenv

# Load .env only in development
if os.getenv("ENVIRONMENT", "production") == "development":
    load_dotenv("")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

TRANSMISSION = {
    "host": os.getenv("TRANSMISSION_HOST"),
    "port": int(os.getenv("TRANSMISSION_PORT", 9091)),  # Default to 9091
    "username": os.getenv("TRANSMISSION_USERNAME"),
    "password": os.getenv("TRANSMISSION_PASSWORD"),
}

RADARR_BASE_URL = os.getenv("RADARR_BASE_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")

SONARR_BASE_URL = os.getenv("SONARR_BASE_URL")
SONARR_API_KEY = os.getenv("SONARR_API_KEY")

ORBITAL_BASE_URL = os.getenv("ORBITAL_BASE_URL")
