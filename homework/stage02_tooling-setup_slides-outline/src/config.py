# src/config.py

import os
from dotenv import load_dotenv

def load_environment():

    # Loads environment variables from a .env file.
    # Call this function at the start of your scripts.

    load_dotenv()

def get_api_key():

    # Retrieves the API_KEY from the environment variables.

    # Returns str: The API key, or None if it's not set.

    return os.getenv("API_KEY")

def get_data_dir():

    # Retrieves the DATA_DIR from the environment variables.

    # Returns str: The data directory path, or None if it's not set.

    return os.getenv("DATA_DIR")