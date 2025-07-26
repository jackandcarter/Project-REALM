"""Simple placeholder NPC brain using a language model API."""

from typing import Any, Dict, List

# In a real implementation this would call into OpenAI or another model
# to generate an NPC response. Here we use a simple echo for demonstration.


def generate_response(npc_id: str, prompt: str) -> str:
    """Generate a text response for an NPC given a prompt."""
    # Placeholder for LLM call, e.g., openai.ChatCompletion.create(...)
    return f"NPC {npc_id} replies: {prompt}"


class NpcBrain:
    """Placeholder NPC brain that will eventually use AXLearn and LoRA."""

    async def generate_response(
        self,
        npc_id: str,
        player_id: str,
        text: str,
        memory: List[Dict[str, Any]],
    ) -> str:
        """Return an NPC response for the given input.

        The current implementation simply echoes the player's text. Once
        AXLearn is integrated, this method will invoke the language model and
        utilize the provided ``memory`` context.
        """

        # TODO: Replace with AXLearn model call and apply LoRA adapter weights.
        return f"NPC {npc_id} echoes to {player_id}: {text}"

    def reset_adapter(self, npc_id: str) -> None:
        """Reset or remove the LoRA adapter for the NPC.

        This placeholder does nothing. Adapter loading and unloading logic will
        be implemented once LoRA support is added.
        """

        # TODO: Remove or reset LoRA weights for the given NPC.
        return None
