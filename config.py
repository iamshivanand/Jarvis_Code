import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- General Settings ---
USER_ID = os.getenv("USER_ID", "default_user")
CREATOR_NAME = os.getenv("CREATOR_NAME", "Creator")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")

# --- File System Settings ---
# A comma-separated list of directories to index for file searches.
# Example: "C:/Users/YourUser/Documents,D:/Media"
SEARCH_DIRECTORIES_STR = os.getenv("SEARCH_DIRECTORIES", "D:/")
SEARCH_DIRECTORIES = [path.strip() for path in SEARCH_DIRECTORIES_STR.split(',')]

# --- Application Mappings ---
# A JSON string that maps simple names to application commands or paths.
DEFAULT_APP_MAPPINGS = {
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": "chrome",
    "vlc": "vlc",
    "command prompt": "cmd",
    "control panel": "control",
    "settings": "start ms-settings:",
    "paint": "mspaint",
    "vs code": "code",
    "postman": "postman"
}
APP_MAPPINGS_JSON = os.getenv("APP_MAPPINGS", json.dumps(DEFAULT_APP_MAPPINGS))
try:
    APP_MAPPINGS = json.loads(APP_MAPPINGS_JSON)
except json.JSONDecodeError:
    print("Warning: Invalid JSON in APP_MAPPINGS environment variable. Using default.")
    APP_MAPPINGS = DEFAULT_APP_MAPPINGS

# --- Security Settings ---
# A secret token to activate the keyboard and mouse controller.
# It's recommended to set this to a secure, random string in your .env file.
CONTROLLER_ACTIVATION_TOKEN = os.getenv("CONTROLLER_ACTIVATION_TOKEN", "my_secret_token")

# --- API Keys (loaded directly from environment) ---
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# You can add logging or validation here if needed
if not all([LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL, GOOGLE_API_KEY]):
    print("Warning: One or more critical API keys (LiveKit, Google AI) are missing.")
