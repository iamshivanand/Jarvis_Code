import os
import subprocess
import sys
import logging
import asyncio
from fuzzywuzzy import process
from langchain.tools import tool
from utils import focus_window
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Helper Functions (Internal) ---

def _blocking_index_items(base_dirs):
    """Synchronous function to perform file and folder indexing."""
    item_index = []
    for base_dir in base_dirs:
        try:
            for root, dirs, files in os.walk(base_dir):
                for d in dirs:
                    item_index.append({"name": d, "path": os.path.join(root, d), "type": "folder"})
                for f in files:
                    item_index.append({"name": f, "path": os.path.join(root, f), "type": "file"})
        except FileNotFoundError:
            logger.warning(f"Directory not found, skipping: {base_dir}")
            continue
    logger.info(f"Indexed {len(item_index)} items from {base_dirs}.")
    return item_index

async def _index_items_async():
    """Asynchronously indexes items from configured directories."""
    return await asyncio.to_thread(_blocking_index_items, config.SEARCH_DIRECTORIES)

async def _search_item(name: str, item_type: str = None):
    """Searches for a file or folder by name."""
    index = await _index_items_async()

    if item_type:
        filtered_index = [item for item in index if item['type'] == item_type]
    else:
        filtered_index = index

    choices = [item["name"] for item in filtered_index]
    if not choices:
        return None

    best_match, score = process.extractOne(name, choices)
    logger.info(f"Matched '{name}' to '{best_match}' with score {score}")

    if score > 70:
        for item in filtered_index:
            if item["name"] == best_match:
                return item
    return None

# --- Agent Tools ---

@tool
async def open_item(name: str) -> str:
    """
    Opens a file or folder by its name.
    Searches in the configured directories.
    """
    item = await _search_item(name)
    if not item:
        return f"❌ Could not find a file or folder named '{name}'."

    try:
        path = item['path']
        logger.info(f"Opening {item['type']}: {path}")
        if os.name == 'nt':
            os.startfile(path)
        else:
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path])

        await focus_window(item["name"])
        return f"✅ Successfully opened {item['type']}: {item['name']}"
    except Exception as e:
        logger.error(f"Error opening item {name}: {e}")
        return f"❌ Failed to open {item['name']}: {e}"

@tool
async def create_folder(name: str) -> str:
    """
    Creates a new folder in the first configured search directory.
    """
    if not config.SEARCH_DIRECTORIES:
        return "❌ Cannot create folder: No search directories are configured."

    base_path = config.SEARCH_DIRECTORIES[0]
    path = os.path.join(base_path, name)

    try:
        os.makedirs(path, exist_ok=True)
        return f"✅ Folder '{name}' created successfully at {path}."
    except Exception as e:
        logger.error(f"Error creating folder {name}: {e}")
        return f"❌ Failed to create folder '{name}': {e}"

@tool
async def rename_item(old_name: str, new_name: str) -> str:
    """
    Renames a file or folder.
    """
    item = await _search_item(old_name)
    if not item:
        return f"❌ Could not find a file or folder named '{old_name}' to rename."

    old_path = item['path']
    new_path = os.path.join(os.path.dirname(old_path), new_name)

    try:
        os.rename(old_path, new_path)
        return f"✅ Renamed '{old_name}' to '{new_name}'."
    except Exception as e:
        logger.error(f"Error renaming item {old_name}: {e}")
        return f"❌ Failed to rename '{old_name}': {e}"

@tool
async def delete_item(name: str) -> str:
    """
    Deletes a file or folder. Use with caution.
    """
    item = await _search_item(name)
    if not item:
        return f"❌ Could not find a file or folder named '{name}' to delete."

    path = item['path']
    item_type = item['type']

    try:
        if item_type == 'folder':
            # Be careful with rmdir, it only works on empty directories.
            # For a more powerful delete, one might use shutil.rmtree, but that's dangerous.
            os.rmdir(path)
        else:
            os.remove(path)
        return f"🗑️ Successfully deleted {item_type}: {name}."
    except OSError as e:
        logger.error(f"Error deleting {item_type} {name}: {e}")
        return f"❌ Failed to delete '{name}'. It might not be empty or there's a permission issue."
    except Exception as e:
        logger.error(f"Error deleting {item_type} {name}: {e}")
        return f"❌ Failed to delete '{name}': {e}"
