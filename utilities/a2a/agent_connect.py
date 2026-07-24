# from  a2a.types import AgentCard, Task, SendMessageRequest

# import httpx
# from typing import Any
# import uuid


# class AgentConnector:
#     """
#     Connects to remote A2A agent and provides a uniform method to delegate tasks.

#      The host agent will orchastrate the tasks that it gets. Lists out all the available agents. Then get the agent cards and understand the agents skills.
#      Then the host agent may decide to call one of the agent and that call from host to the agent is handled by the agent connector.
#     """
#     def __init__(self, agent_card: AgentCard):
#         self.agent_card = agent_card

#     async def send_task(self, message: str, session_id: str) -> Task:
#         """
#         Send a task to the agent and return the Task object

#         Args:
#             message (str): The message to send to the agent
#             session_id (str): The session ID for tracking the task
        
#         returns:
#             Task: The Task object containing the response from the agent
#         """

#         async with httpx.AsyncClient(timeout = 300.0) as httpx_client:
#             a2a_client = A2AClient(
#                 httpx_client = httpx_client,
#                 agent_card = self.agent_card
#             )

#             send_message_payload: dict[str, Any] = {
#                 'message': {
#                     'role': 'user',
#                     'parts':[
#                         {
#                             'text': message,
#                             'kind': 'text'
#                         }
#                     ]
#                 }
#             }



import uuid
from typing import AsyncGenerator, Optional

import grpc
import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import get_artifact_text, get_message_text
from a2a.types import (
    AgentCard,
    Message,
    Part,
    Role,
    SendMessageRequest,
    StreamResponse,
)


class AgentConnector:
    """Connector class to interact with an A2A Agent server (v1.0 SDK compliant)."""

    def __init__(self, agent_url: str, transport: Optional[str] = None) -> None:
        """
        :param agent_url: Base URL of the agent (e.g., 'http://127.0.0.1:41241')
        :param transport: Transport protocol, e.g., 'JSONRPC', 'HTTP+JSON', or 'GRPC'
        """
        self.agent_url = agent_url
        self.transport = transport
        self.card: Optional[AgentCard] = None
        self.client = None

    async def connect(self) -> None:
        """Resolves the AgentCard and initializes the A2A Client connection."""
        config = ClientConfig(
            grpc_channel_factory=grpc.aio.insecure_channel,
        )
        if self.transport:
            config.supported_protocol_bindings = [self.transport]

        # 1. Resolve Agent Card from host
        async with httpx.AsyncClient() as httpx_client:
            resolver = A2ACardResolver(httpx_client, self.agent_url)
            self.card = await resolver.get_agent_card()

        # 2. Instantiate v1.0 Client via factory helper
        self.client = await create_client(self.card, client_config=config)

    async def send_message(
        self,
        text: str,
        task_id: Optional[str] = None,
        context_id: Optional[str] = None,
    ) -> AsyncGenerator[StreamResponse, None]:
        """Sends a message to the agent and yields raw StreamResponse objects."""
        if not self.client:
            raise RuntimeError("Connector is not connected. Call `connect()` first.")

        # Construct Protobuf Message using v1.0 conventions
        message = Message(
            role=Role.ROLE_USER,  # Enum uses SCREAMING_SNAKE_CASE
            message_id=str(uuid.uuid4()),
            parts=[Part(text=text)],  # Direct construction without intermediate wrappers
            task_id=task_id,
            context_id=context_id or str(uuid.uuid4()),
        )

        request = SendMessageRequest(message=message)

        # send_message returns AsyncIterator[StreamResponse] in v1.0
        async for chunk in self.client.send_message(request):
            yield chunk

    async def close(self) -> None:
        """Closes the active client session."""
        if self.client:
            await self.client.close()
            self.client = None