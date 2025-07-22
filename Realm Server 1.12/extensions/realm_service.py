from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql.models.realm_models import Realm
import json
import os

app = Flask(__name__)


def _load_config() -> dict:
    """Load configuration from the central config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    with open(config_path, "r") as file:
        return json.load(file)


config = _load_config()

# Database connection
DATABASE_URL = (
    f"mysql+pymysql://{config['mysql_user']}:{config['mysql_password']}"
    f"@{config['mysql_host']}/{config['databases']['realms']}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route("/realms", methods=["GET"])
def get_realms():
    """Fetch a list of realms, optionally filtered by type."""
    session = Session()
    realm_type = request.args.get("type")  # Filter by type (PVP, PVE, etc.)
    
    try:
        query = session.query(Realm)
        if realm_type:
            query = query.filter(Realm.realm_type == realm_type)

        realms = query.all()
        return jsonify([
            {
                "id": realm.id,
                "name": realm.name,
                "type": realm.realm_type,
                "ip_address": realm.ip_address,
                "port": realm.port,
                "is_online": realm.is_online,
                "max_players": realm.max_players,
                "current_players": realm.current_players,
            } for realm in realms
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/realm/<int:realm_id>/status", methods=["GET"])
def get_realm_status(realm_id):
    """Get the status of a specific realm by ID."""
    session = Session()

    try:
        realm = session.query(Realm).filter(Realm.id == realm_id).first()
        if realm:
            return jsonify({
                "id": realm.id,
                "name": realm.name,
                "is_online": realm.is_online,
                "current_players": realm.current_players,
                "max_players": realm.max_players,
            })
        else:
            return jsonify({"error": "Realm not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
