import json
import os

CONFIG_FILE = "config.json"

def get_mysql_credentials():
    """Load MySQL credentials or prompt user for them."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file).get("mysql")

    # Prompt for credentials if not found
    credentials = {
        "host": input("Enter MySQL host (default: localhost): ") or "localhost",
        "user": input("Enter MySQL user (default: root): ") or "root",
        "password": input("Enter MySQL password: "),
    }

    # Save credentials to config.json
    with open(CONFIG_FILE, "w") as file:
        json.dump({"mysql": credentials}, file, indent=4)

    return credentials
