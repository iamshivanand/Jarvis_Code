"""
This module collects all the individual tool functions from across the application
and provides them as a single list to be used by the main agent.
"""

# Foundational tools
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather

# Newly refactored tool modules
from app_control_tools import open_app, close_app
from file_system_tools import open_item, create_folder, rename_item, delete_item

# GUI automation tools
from keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool,
)

# A single list containing all the tools that the agent can use.
# This list will be passed to the agent in agent.py.
all_tools = [
    # Web and information tools
    google_search,
    get_current_datetime,
    get_weather,
    
    # Application control tools
    open_app,
    close_app,
    
    # File system tools
    open_item,
    create_folder,
    rename_item,
    delete_item,
    
    # Low-level GUI control tools
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    press_hotkey_tool,
    control_volume_tool,
    swipe_gesture_tool,
]