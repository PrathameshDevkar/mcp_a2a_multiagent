from __future__ import annotations

import json
from pathlib import Path
from typing import List
import logging
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools import AgentTool

from pydantic import BaseModel, Field, ValidationError
import os 
logger = logging.getLogger(__name__)


#Registry Models
class AgentRegistryEntry(BaseModel):
    """
    one remote A2A agent.
    """

    name: str = Field(description = "Unique name of the remote agent.")
    agent_card: str = Field(description = "URL or local path to the Agent card")
    description: str = Field(default= "",description = "Optional local description override.")

class AgentRegistry(BaseModel):
    agents: list[AgentRegistryEntry]


#Factory
class RemoteA2aAgentFactory:
    """
    Factory responsible for creating ADK AgentT
    from remote A2a agent registrations.

    Responsibilities:
    1. Read agent_registry.json
    2. Create RemoteA2aAgent
    3. wrap it using AgentTool
    4. return list of tools

    it intentionally does not:
        - perform messaging
        - manage sessions
        - perform discovery
        - cache responses

    Those responsibilities belongs to ADK
    """

    def __init__(self,registry_path: str | Path):
        self.registry_path = registry_path
        self._tools: list[AgentTool] | None = None

    async def get_tools(self) -> List[AgentTool]:
        """
        Returns all AgentTools.
        Tools are created only once.
        """
        if self._tools is not None:
            return self._tools

        registry = self._load_registry()

        tools: List[AgentTool] = []

        for entry in registry.agents:
            remote_agent = RemoteA2aAgent(
                name = entry.name,
                description  = entry.description,
                agent_card = entry.agent_card
            )

            tools.append(
                AgentTool(agent = remote_agent)
            )
            logger.info(
                "Loaded Remote a2a agent: %s",
                entry.name
            )
        
        self._tools = tools

        logger.info(
            "Loaded Remote a2a agents: %s",
            len(tools)
        )

        return tools

    def clear_cache(self):
        self._tools = None

    def _load_registry(self) -> AgentRegistry:
        """
        Loads the agent registry file.
        """
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(
                f"Agent registry not found: {self.registry_path}"
            )
        
        with open(self.registry_path,"r", encoding = "utf-8") as f:
            data= json.load(f)

        try:
            return AgentRegistry.model_validate(data)

        except ValidationError as e:
            raise RuntimeError(
                "Invalid agent_registry.json"
            ) from e
