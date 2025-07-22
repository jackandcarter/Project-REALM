import json
import importlib.util
import os

MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "config_manager.py")
spec = importlib.util.spec_from_file_location("config_manager", MODULE_PATH)
config_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_manager)


def test_get_mysql_credentials_reads_new_format(tmp_path, monkeypatch):
    cfg = {
        "mysql_user": "tester",
        "mysql_password": "secret",
        "mysql_host": "db.example.com",
        "mysql_port": 3307,
    }
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg))
    monkeypatch.setattr(config_manager, "CONFIG_FILE", str(cfg_path))

    creds = config_manager.get_mysql_credentials()

    assert creds == {
        "host": "db.example.com",
        "user": "tester",
        "password": "secret",
        "port": 3307,
    }
