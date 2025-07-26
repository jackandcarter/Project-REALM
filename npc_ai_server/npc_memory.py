import datetime
import json
import os
from typing import Any, Dict, List

# Directory where NPC interaction logs are stored.
LOG_DIR = "npc_memory_logs"


def store_memory(npc_id: str, event: dict) -> None:
    """Append a memory event for an NPC to its JSONL log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    entry = {"timestamp": datetime.datetime.utcnow().isoformat(), **event}
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_memory(npc_id: str) -> List[Dict[str, Any]]:
    """Load all memory events for an NPC.

    Each line of ``npc_memory_logs/{npc_id}.jsonl`` is a JSON object with the
    keys ``timestamp``, ``player_id``, ``input``, and ``response``.
    """
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    if not os.path.exists(log_path):
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def log_interaction(npc_id: str, player_id: str, input_text: str, response: str) -> None:
    """Log a single NPC interaction.

    Each line in ``npc_memory_logs/{npc_id}.jsonl`` contains a JSON object with
    the keys ``timestamp``, ``player_id``, ``input``, and ``response``.
    The timestamp is recorded in UTC ISO 8601 format.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "player_id": player_id,
        "input": input_text,
        "response": response,
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def reset_memory(npc_id: str) -> None:
    """Delete the NPC's interaction log and any adapter file.

    Removes ``npc_memory_logs/{npc_id}.jsonl`` and any files in
    ``models/adapters`` that start with the NPC ID.
    """
    log_path = os.path.join(LOG_DIR, f"{npc_id}.jsonl")
    if os.path.exists(log_path):
        os.remove(log_path)

    adapter_dir = os.path.join(os.path.dirname(__file__), "models", "adapters")
    if os.path.isdir(adapter_dir):
        for fname in os.listdir(adapter_dir):
            if fname.startswith(npc_id):
                try:
                    os.remove(os.path.join(adapter_dir, fname))
                except FileNotFoundError:
                    pass
