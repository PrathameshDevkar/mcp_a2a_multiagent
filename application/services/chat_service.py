from __future__ import annotations

from collections.abc import AsyncIterator

from google.adk.events import Event

from mcp_a2a_multiagent.application.runtime.host_runtime import HostRunTime
from mcp_a2a_multiagent.utilities.logger import debug_log

class ChatService:
    """
    Application service responsible for executing user's chat requests.

    Responsibilities:
        - Accepts user's chat request
        - Invoke the hostruntime
        - Convert ADK events into streamed text response.
    """

    def __init__(self, runtime: HostRunTime):
        self._runtime = runtime

    async def stream_chat(
        self, 
        *,
        session_id: str,
        user_id: str,
        message: str
    ) -> AsyncIterator[str]:
        """
        Executes the user chat request and stream the generated response.
        """

        async for event in self._runtime.run(
            session_id = session_id,
            user_id = user_id,
            message = message
        ):
            debug_log(
                component="ChatService",
                message="Runtime runner Event",
                obj=event,
            )
            text = self._extract_text(event=event)

            if text:
                yield text
    
    @staticmethod
    def _extract_text(event: Event) -> str | None:
        """
        Extracts the generated text from the ADK event
        """

        if (
            event.content 
            and event.content.parts
            and event.content.parts[-1].text
        ):
            return event.content.parts[-1].text
        
        return None