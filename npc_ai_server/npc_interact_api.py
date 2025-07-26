# coding: utf-8
"""FastAPI application exposing NPC interaction endpoints."""

from fastapi import FastAPI
from pydantic import BaseModel

from .npc_brain import NpcBrain
from . import npc_memory

app = FastAPI(title="NPC Interaction API")

# Global brain instance reused across requests
brain = NpcBrain()


class InteractRequest(BaseModel):
    """Request body for interacting with an NPC."""

    npc_id: str
    player_id: str
    input_text: str


class ResetRequest(BaseModel):
    """Request body for resetting an NPC's state."""

    npc_id: str


@app.post("/interact")
async def interact(req: InteractRequest):
    """Generate an NPC response using its conversation memory."""

    # Load previous memory/events for context
    memory = npc_memory.load_memory(req.npc_id)

    # Use the brain to generate the next response
    response = await brain.generate_response(
        req.npc_id, req.player_id, req.input_text, memory
    )

    # Log the interaction for future context
    npc_memory.log_interaction(
        req.npc_id, req.player_id, req.input_text, response
    )

    return {"response": response}


@app.post("/reset")
async def reset(req: ResetRequest):
    """Clear an NPC's memory and adapter weights."""

    npc_memory.reset_memory(req.npc_id)
    brain.reset_adapter(req.npc_id)
    return {"status": "reset"}


if __name__ == "__main__":
    import uvicorn

    # Run the API with uvicorn when executed directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
