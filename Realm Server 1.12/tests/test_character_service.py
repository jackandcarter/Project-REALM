import importlib.util
import os
import pytest

MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "extensions", "world_service.py")
spec = importlib.util.spec_from_file_location("world_service", MODULE_PATH)
world_service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(world_service)

world_service.app.testing = True

class DummyCursor:
    def __init__(self, fetch=None, rowcount=1):
        self.executed = []
        self.fetch = fetch
        self.rowcount = rowcount
        self.lastrowid = 1

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchall(self):
        return self.fetch

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class DummyConnection:
    def __init__(self, fetch=None, rowcount=1):
        self.cursor_obj = DummyCursor(fetch, rowcount)

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass

@pytest.fixture
def client():
    return world_service.app.test_client()


def test_create_character(monkeypatch, client):
    conn = DummyConnection()
    monkeypatch.setattr(world_service, "get_db_connection", lambda: conn)
    resp = client.post("/characters", json={"account_id":1,"name":"Hero","class_id":2,"appearance":"a"})
    assert resp.status_code == 201
    assert any("INSERT INTO characters" in q[0] for q in conn.cursor_obj.executed)


def test_list_characters(monkeypatch, client):
    data = [{"id":1,"account_id":1,"name":"Hero","class_id":2,"appearance":"a"}]
    conn = DummyConnection(fetch=data)
    monkeypatch.setattr(world_service, "get_db_connection", lambda: conn)
    resp = client.get("/characters/1")
    assert resp.status_code == 200
    assert resp.get_json() == data


def test_update_character(monkeypatch, client):
    conn = DummyConnection()
    monkeypatch.setattr(world_service, "get_db_connection", lambda: conn)
    resp = client.put("/characters/5", json={"class_id":3,"appearance":"b"})
    assert resp.status_code == 200
    updates = [q for q in conn.cursor_obj.executed if "UPDATE characters" in q[0]]
    assert len(updates) == 1


def test_delete_character(monkeypatch, client):
    conn = DummyConnection(rowcount=1)
    monkeypatch.setattr(world_service, "get_db_connection", lambda: conn)
    resp = client.delete("/characters/5")
    assert resp.status_code == 200
    dels = [q for q in conn.cursor_obj.executed if "DELETE FROM characters" in q[0]]
    assert len(dels) == 1


def test_delete_character_not_found(monkeypatch, client):
    conn = DummyConnection(rowcount=0)
    monkeypatch.setattr(world_service, "get_db_connection", lambda: conn)
    resp = client.delete("/characters/99")
    assert resp.status_code == 404
