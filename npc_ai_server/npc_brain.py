"""Simple placeholder NPC brain using a language model API."""

from typing import Any

# In a real implementation this would call into OpenAI or another model
# to generate an NPC response. Here we use a simple echo for demonstration.


def generate_response(npc_id: str, prompt: str) -> str:
    """Generate a text response for an NPC given a prompt."""
    # Placeholder for LLM call, e.g., openai.ChatCompletion.create(...)
    return f"NPC {npc_id} replies: {prompt}"
