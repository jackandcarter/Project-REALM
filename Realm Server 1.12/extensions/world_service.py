from flask import Flask, jsonify, request
import pymysql
import logging
import json
import os


app = Flask(__name__)

# Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/world_service.log"),
        logging.StreamHandler(),
    ],
)


def _load_config() -> dict:
    """Load configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path, "r") as file:
        return json.load(file)


def get_db_connection():
    """Create a connection to the world database."""
    config = _load_config()
    return pymysql.connect(
        host=config["mysql_host"],
        user=config["mysql_user"],
        password=config["mysql_password"],
        database=config["databases"]["world"],
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/characters", methods=["POST"])
def create_character():
    """Create a new character."""
    data = request.json or {}
    account_id = data.get("account_id")
    name = data.get("name")
    class_id = data.get("class_id")
    appearance = data.get("appearance", "")
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO characters (account_id, name, class_id, appearance) VALUES (%s, %s, %s, %s)",
                (account_id, name, class_id, appearance),
            )
            character_id = cursor.lastrowid
        connection.commit()
        return jsonify({"id": character_id}), 201
    finally:
        connection.close()


@app.route("/characters/<int:account_id>", methods=["GET"])
def list_characters(account_id: int):
    """List all characters for an account."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM characters WHERE account_id = %s",
                (account_id,),
            )
            chars = cursor.fetchall()
        return jsonify(chars)
    finally:
        connection.close()


@app.route("/characters/<int:char_id>", methods=["PUT"])
def update_character(char_id: int):
    """Update a character's appearance or class."""
    data = request.json or {}
    appearance = data.get("appearance")
    class_id = data.get("class_id")
    if appearance is None and class_id is None:
        return jsonify({"error": "No data provided"}), 400
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if appearance is not None and class_id is not None:
                cursor.execute(
                    "UPDATE characters SET appearance = %s, class_id = %s WHERE id = %s",
                    (appearance, class_id, char_id),
                )
            elif appearance is not None:
                cursor.execute(
                    "UPDATE characters SET appearance = %s WHERE id = %s",
                    (appearance, char_id),
                )
            elif class_id is not None:
                cursor.execute(
                    "UPDATE characters SET class_id = %s WHERE id = %s",
                    (class_id, char_id),
                )
        connection.commit()
        return jsonify({"status": "success"})
    finally:
        connection.close()


@app.route("/characters/<int:char_id>", methods=["DELETE"])
def delete_character(char_id: int):
    """Delete a character."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM characters WHERE id = %s", (char_id,))
            affected = cursor.rowcount
        connection.commit()
        if affected:
            return jsonify({"status": "deleted"})
        return jsonify({"error": "Character not found"}), 404
    finally:
        connection.close()

@app.route("/world/map/<int:map_id>", methods=["GET"])
def get_map(map_id: int):
    """Retrieve map data for the given map ID."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
            map_data = cursor.fetchone()
        if map_data:
            logging.info(f"Map {map_id} retrieved")
            return jsonify(map_data)
        logging.warning(f"Map {map_id} not found")
        return jsonify({"error": "Map not found"}), 404
    finally:
        connection.close()


@app.route("/world/player/<int:player_id>/location", methods=["GET"])
def get_player_location(player_id: int):
    """Get the current location for a player."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT map_id, x, y, z FROM player_positions WHERE player_id = %s",
                (player_id,),
            )
            position = cursor.fetchone()
        if position:
            logging.info(f"Location for player {player_id} fetched")
            return jsonify(position)
        logging.warning(f"Player {player_id} location not found")
        return jsonify({"error": "Player not found"}), 404
    finally:
        connection.close()


@app.route("/world/player/<int:player_id>/move", methods=["POST"])
def move_player(player_id: int):
    """Update a player's world location."""
    data = request.json or {}
    x = data.get("x")
    y = data.get("y")
    z = data.get("z")
    map_id = data.get("map_id")
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "REPLACE INTO player_positions (player_id, map_id, x, y, z) VALUES (%s, %s, %s, %s, %s)",
                (player_id, map_id, x, y, z),
            )
        connection.commit()
        logging.info(
            f"Player {player_id} moved to ({x}, {y}, {z}) on map {map_id}"
        )
        return jsonify({"status": "success"})
    finally:
        connection.close()


if __name__ == "__main__":
    logging.info("World Service starting...")
    app.run(host="127.0.0.1", port=5003)

