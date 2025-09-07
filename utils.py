import asyncio
import logging
import httpx

try:
    import pygetwindow as gw
except ImportError:
    gw = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_current_city() -> str:
    """
    Asynchronously gets the current city based on IP address using ipinfo.io.
    """
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("https://ipinfo.io/json")
            response.raise_for_status()
            data = response.json()
            return data.get("city", "Unknown")
    except httpx.RequestError as e:
        logger.error(f"Error while fetching current city: {e}")
        return "Unknown"
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching city: {e}")
        return "Unknown"

async def focus_window(title_keyword: str) -> bool:
    """
    Brings a window to the foreground if its title contains the given keyword.
    """
    if not gw:
        logger.warning("pygetwindow is not installed, cannot focus window.")
        return False

    await asyncio.sleep(1.5)  # Give time for the window to appear
    title_keyword = title_keyword.lower().strip()

    try:
        for window in gw.getAllWindows():
            if title_keyword in window.title.lower():
                if window.isMinimized:
                    window.restore()
                window.activate()
                logger.info(f"Successfully focused window: {window.title}")
                return True
        logger.warning(f"No window found with keyword: {title_keyword}")
        return False
    except Exception as e:
        logger.error(f"An error occurred while focusing window: {e}")
        return False
