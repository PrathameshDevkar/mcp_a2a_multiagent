from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Incoming chat request
    """
    user_id :str = Field(description = "Unique user identifier")
    session_id: str = Field(description = "Conversation session identifier")
    message: str = Field(description = "User message")

    