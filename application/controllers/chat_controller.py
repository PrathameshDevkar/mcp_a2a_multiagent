from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from mcp_a2a_multiagent.application.models.request import ChatRequest

router = APIRouter(prefix = "/chat", tags=["Chat"])

@router.post("/")
async def chat(
    request: Request,
    chat_request: ChatRequest
):
    """
    Execute a chat request.
    """

    chat_service = request.app.state.chat_service

    async def event_generator():
        async for chunk in chat_service.stream_chat(
            user_id = chat_request.user_id,
            session_id = chat_request.session_id,
            message = chat_request.message
        ):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type = "text/plain"
    )

