"""FastAPI runtime for NPC interactions."""

from fastapi import FastAPI
from pydantic import BaseModel

from .npc_brain import generate_response
from .npc_memory import store_memory


app = FastAPI(title="NPC Runtime API")


class ChatRequest(BaseModel):
    message: str


@app.post("/npc/{npc_id}/chat")
def chat_with_npc(npc_id: str, request: ChatRequest):
    """Receive a message from a player and return the NPC's response."""
    response = generate_response(npc_id, request.message)
    store_memory(npc_id, {"input": request.message, "response": response})
    return {"npc_id": npc_id, "response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
