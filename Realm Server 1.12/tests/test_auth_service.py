import importlib.util
import os
import pytest

# Ensure log directory exists for auth_service logging
os.makedirs("logs", exist_ok=True)

# Helper classes for mocking database connections
class DummyCursor:
    def __init__(self, user):
        self.user = user
        self.executed = []
        self._fetch = None

    def execute(self, sql, params):
        self.executed.append((sql, params))
        if "SELECT id, is_banned" in sql:
            self._fetch = self.user

    def fetchone(self):
        return self._fetch

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class DummyConnection:
    def __init__(self, user=None):
        self.cursor_obj = DummyCursor(user)

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
    def fake_conn():
        return DummyConnection({"id": 1, "is_banned": 0})

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "user", "password_hash": "pw"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_banned_user(monkeypatch, client):
    def fake_conn():
        return DummyConnection({"id": 2, "is_banned": 1})

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "banned", "password_hash": "pw"})
    assert response.status_code == 403
    assert response.get_json()["status"] == "failed"


def test_invalid_login(monkeypatch, client):
    def fake_conn():
        return DummyConnection(None)

    monkeypatch.setattr(auth_service, "get_db_connection", fake_conn)
    response = client.post("/auth/login", json={"username": "unknown", "password_hash": "pw"})
    assert response.status_code == 401
    assert response.get_json()["status"] == "failed"
