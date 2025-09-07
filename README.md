# Jarvis - An Advanced Voice AI Assistant

Jarvis is a sophisticated, voice-controlled AI assistant designed to be a powerful and interactive companion for your desktop. Built with Python using the `livekit-agents` framework, it leverages modern AI capabilities to understand natural language and perform a wide range of tasks on your computer.

This assistant is not just a chatbot; it's an agent that can perceive, think, and act within your digital environment.

## Features

- **Real-time Voice Conversation:** Engage in natural, low-latency conversations. Jarvis listens and responds in real-time.
- **Intelligent Tool Use:** Powered by a Large Language Model, Jarvis can understand complex commands and decide which of its many tools is the right one for the job.
- **Web Search:** Ask questions about anything, and Jarvis will use Google Search to find the most up-to-date information for you.
- **Application Control:** Launch and close your favorite desktop applications with simple voice commands (e.g., "Open Chrome", "Close Notepad").
- **File System Management:** A complete suite of tools to interact with your files and folders.
  - Open files and folders by name.
  - Create new folders.
  - Rename existing files and folders.
  - Delete items from your file system.
- **GUI Automation:** Take hands-free control of your computer with low-level mouse and keyboard automation.
  - Move the mouse cursor and perform clicks.
  - Scroll up and down on any page.
  - Type text into any active window.
  - Press any key or combination of hotkeys (e.g., Ctrl+S, Alt+F4).
- **Persistent Memory:** Jarvis remembers your past conversations using a robust SQLite database, allowing for contextual follow-ups.
- **Configurable and Personable:** The assistant's name, creator's name, and even its search paths are fully configurable.

## Getting Started

Follow these instructions to get Jarvis running on your local machine.

### Prerequisites

- Python 3.8 or higher.
- Access to a microphone for voice input.

### 1. Clone the Repository

First, clone this repository to your local machine:
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Install Dependencies

Install all the necessary Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

This is the most important step. The assistant relies on several external services and needs API keys to function.

1.  Find the `.env.example` file in the root of the project.
2.  Create a copy of it and name it `.env`.
3.  Open the `.env` file and fill in the values for each variable as described below.

#### Required API Keys

-   `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`: Credentials for your LiveKit instance. You can get these from a self-hosted instance or from [LiveKit Cloud](https://cloud.livekit.io/).
-   `GOOGLE_API_KEY`: Your API key from a Google Cloud project with the Generative AI (Gemini) API enabled.
-   `GOOGLE_SEARCH_API_KEY`, `SEARCH_ENGINE_ID`: Required for the web search functionality. You need to set up a Custom Search Engine in your Google Cloud project to get these.
-   `OPENWEATHER_API_KEY`: A free or paid API key from [OpenWeatherMap](https://openweathermap.org/api) to enable the weather forecast tool.

#### Jarvis Configuration (Optional)

These variables have sensible defaults but can be customized in your `.env` file.

-   `USER_ID`: A unique identifier for the user to keep conversation histories separate. Defaults to `default_user`.
-   `CREATOR_NAME`: The name mentioned in the assistant's introductory prompts. Defaults to `Creator`.
-   `ASSISTANT_NAME`: The name of the assistant. Defaults to `Jarvis`.
-   `SEARCH_DIRECTORIES`: A comma-separated list of full directory paths that Jarvis should search for files (e.g., `"C:/Users/YourUser/Documents,D:/Media"`).
-   `APP_MAPPINGS`: A JSON string that maps simple names to application paths or commands (e.g., `{"vscode": "C:\\path\\to\\code.exe"}`).
-   `CONTROLLER_ACTIVATION_TOKEN`: A secret password-like string required to activate the keyboard and mouse controller. **It is highly recommended to change this to a secure, random string.**

### 4. Run the Application

Once your dependencies are installed and your `.env` file is configured, you can start the assistant by running:
```bash
python agent.py
```

You can now start talking to Jarvis!
