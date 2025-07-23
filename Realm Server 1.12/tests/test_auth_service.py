import importlib.util
import os
import pytest
import bcrypt
from datetime import datetime, timedelta

# Ensure log directory exists for auth_service logging
os.makedirs("logs", exist_ok=True)

# Helper classes for mocking database connections
class DummyCursor:
    def __init__(self, user=None, session=None):
        self.user = user
        self.session = session
        self.executed = []
        self._fetch = None

    def execute(self, sql, params):
        self.executed.append((sql, params))
        if "FROM users" in sql and "SELECT" in sql:
            self._fetch = self.user
        elif "FROM sessions" in sql and "SELECT" in sql:
            self._fetch = self.session

    def fetchone(self):
        return self._fetch

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class DummyConnection:
    def __init__(self, user=None, session=None):
        self.cursor_obj = DummyCursor(user, session)

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass

# Utility to load the auth_service module
MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "extensions", "auth_service.py")
spec = importlib.util.spec_from_file_location("auth_service", MODULE_PATH)
auth_service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auth_service)

auth_service.app.testing = True

@pytest.fixture
def client():
    return auth_service.app.test_client()


def test_successful_login(monkeypatch, client):
    hashed = bcrypt.hashpw(b"pw", bcrypt.gensalt()).decode()

    def fake_conn():
        return DummyConnection({"id": 1, "is_banned": 0, "password_hash": hashed})

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "user", "password": "pw"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_banned_user(monkeypatch, client):
    hashed = bcrypt.hashpw(b"pw", bcrypt.gensalt()).decode()

    def fake_conn():
        return DummyConnection({"id": 2, "is_banned": 1, "password_hash": hashed})

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "banned", "password": "pw"})
    assert response.status_code == 403
    assert response.get_json()["status"] == "failed"


def test_invalid_login(monkeypatch, client):
    def fake_conn():
        return DummyConnection(None)

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "unknown", "password": "pw"})
    assert response.status_code == 401
    assert response.get_json()["status"] == "failed"


def test_register_hashes_password(monkeypatch, client):
    conn = DummyConnection()
    monkeypatch.setattr(auth_service, "get_db_connection", lambda: conn)

    response = client.post("/auth/register", json={"username": "new", "password": "secret"})

    assert response.status_code == 200
    inserted = conn.cursor_obj.executed[0][1]
    stored_hash = inserted[1]
    assert stored_hash != "secret"
    assert bcrypt.checkpw(b"secret", stored_hash.encode())


def test_login_creates_session(monkeypatch, client):
    hashed = bcrypt.hashpw(b"pw", bcrypt.gensalt()).decode()
    conn = DummyConnection({"id": 5, "is_banned": 0, "password_hash": hashed})
    monkeypatch.setattr(auth_service, "get_db_connection", lambda: conn)

    resp = client.post("/auth/login", json={"username": "u", "password": "pw"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "session_key" in data

    inserts = [q for q in conn.cursor_obj.executed if "INSERT INTO sessions" in q[0]]
    assert len(inserts) == 1
    assert inserts[0][1][1] == data["session_key"]


def test_validate_session(monkeypatch, client):
    future = datetime.utcnow() + timedelta(hours=1)

    def fake_conn():
        return DummyConnection(session={"user_id": 7, "expires_at": future})

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    resp = client.post("/auth/validate_session", json={"session_key": "abc"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "valid", "user_id": 7}


def test_logout(monkeypatch, client):
    conn = DummyConnection()
    monkeypatch.setattr(auth_service, "get_db_connection", lambda: conn)

    resp = client.post("/auth/logout", json={"session_key": "abc"})
    assert resp.status_code == 200
    dels = [q for q in conn.cursor_obj.executed if "DELETE FROM sessions" in q[0]]
    assert len(dels) == 1
    assert dels[0][1][0] == "abc"
