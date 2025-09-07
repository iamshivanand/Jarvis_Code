import os
import logging
import httpx
from dotenv import load_dotenv
from langchain.tools import tool
from utils import get_current_city

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
async def get_weather(city: str = "") -> str:
    """
    Gives current weather information for a given city.

    Use this tool when the user asks about weather, rain, temperature, humidity, or wind.
    If no city is given, detect city automatically.

    Example prompts:
    - "आज का मौसम कैसा है?"
    - "Weather बताओ Bangalore का"
    - "क्या बारिश होगी मुंबई में?"
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        logger.error("OpenWeather API key missing है।")
        return "Environment variables में OpenWeather API key नहीं मिली।"

    if not city:
        city = await get_current_city()

    logger.info(f"City के लिए weather fetch किया जा रहा है।: {city}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result = (f"Weather in {city}:\n"
                  f"- Condition: {weather}\n"
                  f"- Temperature: {temperature}°C\n"
                  f"- Humidity: {humidity}%\n"
                  f"- Wind Speed: {wind_speed} m/s")

        logger.info(f"Weather result: \n{result}")
        return result

    except Exception as e:
        logger.exception(f"Weather fetch करते समय exception आया: {e}")
        return "Weather fetch करते समय एक error आया"
    
