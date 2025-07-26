import datetime
import json
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "npc_memory_logs")


def store_memory(npc_id: str, event: dict) -> None:
    """Append a memory event for an NPC to its JSONL log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    entry = {"timestamp": datetime.datetime.utcnow().isoformat(), **event}
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_memory(npc_id: str) -> list:
    """Load all memory events for an NPC."""
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    if not os.path.exists(log_path):
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]
