from __future__ import annotations

from pathlib import Path
from mcp_a2a_multiagent.utilities.logger import debug_log

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from google.adk.events import Event

from mcp_a2a_multiagent.agents.host_agent.agent import HostLlmAgent

from collections.abc import AsyncIterator


class HostRunTime:
    """
    Owns the execution lifecycle of the host ai application.

    Responsibilities:
        - Build the host llm agent
        - Own the ADK runner
        - Own the session service
        - own the memory service
        - own the artifact service
        -Execute the host application

    This class intentionally contains no HTTP logic,
    no routing logic and no business logic.
    """

    def __init__(
        self,
        *,
        app_name = str,
        model = str,
        mcp_config_path = str | Path,
        agent_registry_path = str | Path,
    ) -> None:
        self.app_name = app_name
        self._builder = HostLlmAgent(
            model = model,
            mcp_config_path = mcp_config_path,
            agent_registry_path = agent_registry_path
        )

        self._agent: LlmAgent | None = None
        self._runner: Runner | None = None
        self._session_service = None
        self._memory_service = None
        self._artifact_service = None
        self._initialized = False

    async def initialize(self) -> None:
        """
        Builds the host llm agent and initializes the adk runtime.
        Safe to use multiple times
        """

        if self._initialized:
            return

        # Build the hsot agent
        self._agent = await self._builder.build()

        # Build the ADK services
        self._session_service = InMemorySessionService()
        self._memory_service = InMemoryMemoryService()
        self._artifact_service = InMemoryArtifactService()
        # Build the runner
        self._runner = Runner(
            app_name = self.app_name,
            agent = self._agent,
            artifact_service = self._artifact_service,
            session_service = self._session_service,
            memory_service = self._memory_service
        )

        self._initialized = True

    @property
    def runner(self) -> Runner:
        """
        Returns the initialized Google's ADK Runner.
        """

        if self._runner is None:
            raise RuntimeError(
                "HostRuntime is not initialized."
            )

        return self._runner

    async def run(
        self,
        *,
        user_id: str,
        session_id: str,
        message: str
    ) -> AsyncIterator[Event]:
        """
        Executes the host agent and streams ADK events.

        Parameters:
        user_id: str = User identifier
        session_id: str = conversation/ session identifier
        message: str = user message

        Yields
        -------------
        Events
            Stream of ADK events generated during execution

        """
        if not self._initialized:
            raise RuntimeError(
                "HostRunTime runner is not initialized."
            )

        # Ensure the session exeists
        session = await self._session_service.get_session(
                            app_name = self.app_name,
                            user_id = user_id,
                            session_id = session_id
                            )
        if session:
            print("=============session present==============", session)
        
        if session is None:
            print("=============session not present so creating one=================")
            session = await self._session_service.create_session(
                app_name = self.app_name,
                user_id = user_id,
                session_id = session_id
            )
            print("===================session created=====================",session)

        # Convert the appication message into the ADK content object
        user_content = types.Content(
            role = "user",
            parts = [
                types.Part.from_text(text = message)
            ]
        )

        # Delegate the execution to googles runner
        async for event in self._runner.run_async(
            user_id = user_id,
            session_id = session_id,
            new_message = user_content
        ):
            debug_log(
                component="HostRuntime",
                message="Runner Event",
                obj=event,
            )
            yield event

    async def shutdown(self) -> None:
        """
        Gracefully shut downs the runtime.

        """
        self._initialized = False
