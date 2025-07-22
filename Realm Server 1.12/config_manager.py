import json
import os

CONFIG_FILE = "config.json"

def get_mysql_credentials():
    """Load MySQL credentials from config.json or prompt the user."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            cfg = json.load(file)
        return {
            "host": cfg.get("mysql_host", "localhost"),
            "user": cfg.get("mysql_user", "root"),
            "password": cfg.get("mysql_password", ""),
            "port": cfg.get("mysql_port", 3306),
        }

    # Prompt for credentials if config does not exist
    credentials = {
        "host": input("Enter MySQL host (default: localhost): ") or "localhost",
        "user": input("Enter MySQL user (default: root): ") or "root",
        "password": input("Enter MySQL password: "),
        "port": int(input("Enter MySQL port (default: 3306): ") or 3306),
    }

    with open(CONFIG_FILE, "w") as file:
        json.dump(
            {
                "mysql_user": credentials["user"],
                "mysql_password": credentials["password"],
                "mysql_host": credentials["host"],
                "mysql_port": credentials["port"],
            },
            file,
            indent=4,
        )

    return credentials
