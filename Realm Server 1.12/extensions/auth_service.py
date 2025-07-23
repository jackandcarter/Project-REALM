from flask import Flask, request, jsonify
import pymysql
import logging
import json
import os
import bcrypt
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/auth_service.log"),
        logging.StreamHandler()
    ]
)

# Database Connection Helper
def get_db_connection():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path, "r") as file:
        config = json.load(file)
    return pymysql.connect(
        host=config["mysql_host"],
        user=config["mysql_user"],
        password=config["mysql_password"],
        database=config["databases"]["auth"]
    )

# -------------------------
# User Management APIs
# -------------------------

@app.route("/auth/register", methods=["POST"])
def register_user():
    """Register a new user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    permission_level = data.get("permission_level", 0)

    # Hash the plaintext password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password_hash, permission_level) VALUES (%s, %s, %s)",
                (username, password_hash, permission_level)
            )
        connection.commit()
        logging.info(f"User '{username}' registered successfully.")
        return jsonify({"status": "success", "message": f"User '{username}' registered."})
    except pymysql.IntegrityError:
        logging.warning(f"Registration failed: Username '{username}' already exists.")
        return jsonify({"status": "failed", "message": "Username already exists."}), 400
    finally:
        connection.close()

@app.route("/auth/delete", methods=["DELETE"])
def delete_user():
    """Delete a user."""
    data = request.json
    username = data.get("username")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        connection.commit()
        logging.info(f"User '{username}' deleted.")
        return jsonify({"status": "success", "message": f"User '{username}' deleted."})
    finally:
        connection.close()

@app.route("/auth/update", methods=["PUT"])
def update_user():
    """Update user details."""
    data = request.json
    username = data.get("username")
    new_password_hash = data.get("password_hash")
    new_permission_level = data.get("permission_level")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            if new_password_hash:
                cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (new_password_hash, username))
            if new_permission_level is not None:
                cursor.execute("UPDATE users SET permission_level = %s WHERE username = %s", (new_permission_level, username))
        connection.commit()
        logging.info(f"User '{username}' updated successfully.")
        return jsonify({"status": "success", "message": f"User '{username}' updated."})
    finally:
        connection.close()

# -------------------------
# IP Ban/Whitelist APIs
# -------------------------

@app.route("/auth/ban_ip", methods=["POST"])
def ban_ip():
    """Ban an IP address."""
    data = request.json
    ip_address = data.get("ip_address")
    reason = data.get("reason", "No reason provided")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ip_bans (ip_address, reason) VALUES (%s, %s)", (ip_address, reason))
        connection.commit()
        logging.info(f"IP '{ip_address}' banned for reason: {reason}.")
        return jsonify({"status": "success", "message": f"IP '{ip_address}' banned."})
    finally:
        connection.close()

@app.route("/auth/whitelist_ip", methods=["POST"])
def whitelist_ip():
    """Add an IP address to the whitelist."""
    data = request.json
    ip_address = data.get("ip_address")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ip_whitelist (ip_address) VALUES (%s)", (ip_address,))
        connection.commit()
        logging.info(f"IP '{ip_address}' whitelisted.")
        return jsonify({"status": "success", "message": f"IP '{ip_address}' whitelisted."})
    finally:
        connection.close()

# -------------------------
# Login Handling
# -------------------------

@app.route("/auth/login", methods=["POST"])
def login():
    """Handle user login."""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    ip_address = request.remote_addr

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Retrieve stored password hash and ban status
            cursor.execute("SELECT id, is_banned, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
                if user["is_banned"]:
                    logging.warning(f"Banned user '{username}' attempted to log in.")
                    return jsonify({"status": "failed", "message": "User is banned."}), 403

                # Log successful login
                cursor.execute(
                    "INSERT INTO login_history (user_id, ip_address, successful) VALUES (%s, %s, TRUE)",
                    (user["id"], ip_address)
                )
                # Create session for the user
                session_key = secrets.token_hex(32)
                expires_at = datetime.utcnow() + timedelta(hours=1)
                cursor.execute(
                    "INSERT INTO sessions (user_id, session_key, ip_address, expires_at) VALUES (%s, %s, %s, %s)",
                    (user["id"], session_key, ip_address, expires_at),
                )
                connection.commit()
                logging.info(
                    f"User '{username}' logged in successfully from IP {ip_address}."
                )
                return jsonify(
                    {
                        "status": "success",
                        "message": "Login successful.",
                        "session_key": session_key,
                    }
                )
            else:
                # Log failed login
                cursor.execute(
                    "INSERT INTO login_history (user_id, ip_address, successful) VALUES (NULL, %s, FALSE)",
                    (ip_address,)
                )
                connection.commit()
                logging.warning(f"Failed login attempt for username '{username}' from IP {ip_address}.")
                return jsonify({"status": "failed", "message": "Invalid username or password."}), 401
    finally:
        connection.close()


@app.route("/auth/validate_session", methods=["POST"])
def validate_session():
    """Validate an existing session key."""
    session_key = request.json.get("session_key")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, expires_at FROM sessions WHERE session_key = %s",
                (session_key,),
            )
            session = cursor.fetchone()
        if session and session["expires_at"] > datetime.utcnow():
            return jsonify({"status": "valid", "user_id": session["user_id"]})
        return jsonify({"status": "invalid"}), 401
    finally:
        connection.close()


@app.route("/auth/logout", methods=["POST"])
def logout():
    """Invalidate a session key by removing it from the database."""
    session_key = request.json.get("session_key")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sessions WHERE session_key = %s",
                (session_key,),
            )
        connection.commit()
        return jsonify({"status": "success", "message": "Logged out"})
    finally:
        connection.close()

if __name__ == "__main__":
    logging.info("Auth Service starting...")
    app.run(host="127.0.0.1", port=5001)
