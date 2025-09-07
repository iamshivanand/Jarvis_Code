import asyncio
import logging
import sys
try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None
    win32con = None
from langchain.tools import tool
import config
from utils import focus_window

# Setup encoding and logger
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App command map is now loaded from config
APP_MAPPINGS = config.APP_MAPPINGS

@tool
async def open_app(app_title: str) -> str:
    """
    Launches a desktop app like Notepad, Chrome, VLC, etc., based on a pre-configured list.

    Use this tool when the user asks to launch an application on their computer.
    Example prompts:
    - "Notepad खोलो"
    - "Chrome open करो"
    - "VLC media player चलाओ"
    """
    app_title = app_title.lower().strip()
    app_command = APP_MAPPINGS.get(app_title, app_title)
    try:
        # Using asyncio.create_subprocess_shell for non-blocking execution
        await asyncio.create_subprocess_shell(f'start "" "{app_command}"', shell=True)

        focused = await focus_window(app_title)
        if focused:
            return f"🚀 App '{app_title}' launched and focused."
        else:
            return f"🚀 App '{app_title}' launched, but could not be focused."
    except Exception as e:
        logger.error(f"Failed to launch app '{app_title}': {e}")
        return f"❌ Could not launch '{app_title}': {e}"

@tool
async def close_app(window_title: str) -> str:
    """
    Closes an application window by its title. This is a Windows-only feature.

    Use this tool when the user wants to close any app or window on their desktop.
    Example prompts:
    - "Notepad बंद करो"
    - "Close VLC"
    - "Chrome की window बंद कर दो"
    """
    if not win32gui:
        return "❌ This feature is only available on Windows."

    closed = False
    def enumHandler(hwnd, _):
        nonlocal closed
        if win32gui.IsWindowVisible(hwnd):
            if window_title.lower() in win32gui.GetWindowText(hwnd).lower():
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                logger.info(f"Sent WM_CLOSE to window: {win32gui.GetWindowText(hwnd)}")
                closed = True

    win32gui.EnumWindows(enumHandler, None)

    if closed:
        return f"✅ Sent close command to window(s) matching '{window_title}'."
    else:
        return f"❌ Could not find any open window with the title '{window_title}'."
