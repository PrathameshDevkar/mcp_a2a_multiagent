from __future__ import annotations

from pathlib import Path

from google.adk.agents import LlmAgent

from mcp_a2a_multiagent.utilities.a2a.remote_a2a_agent_factory import RemoteA2aAgentFactory
from mcp_a2a_multiagent.agents.host_agent.prompt import HOST_AGENT_INSTRUCTIONS
from mcp_a2a_multiagent.utilities.mcp.mcp_connect import MCPConnector
import os

import vertexai
from vertexai.agent_engines import AdkApp
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Prathamesh\prathamesh\ai_agent\vertexai-free-credits-api-key.json"
vertexai.init(project = "poised-cortex-462609-n4", location = "us-central1")


class HostLlmAgent:
    """
    Responsible for creating the host llm agent.

    Responsibilities:
        - Load MCP tools
        - Load remote A2a agent tools
        - Assemble the host llm agent

    This class intentionally contains no business logic
    """

    def __init__(
        self,
        model: str,
        mcp_config_path: str | Path,
        agent_registry_path: str | Path
    ):
        self.model = model  
        
        self.mcp_connector = MCPConnector(config_file = mcp_config_path)

        self.a2a_factory = RemoteA2aAgentFactory(registry_path = agent_registry_path)

    async def build(self) -> LlmAgent:
        """
        Builds and returns the host llm agent.
        """

        # Load MPC tools
        mcp_tools = await self.mcp_connector.get_toolsets()

        # Load a2a factory tools
        a2a_tools = await self.a2a_factory.get_tools()

        # Combine all tools
        tools = [
            *mcp_tools,
            *a2a_tools
        ]

        # Create Host Agent
        host_agent = LlmAgent(
            name = "host_agent",
            model = self.model,
            instruction = HOST_AGENT_INSTRUCTIONS,
            tools = tools
        )
        agent = AdkApp(agent= host_agent)
        return host_agent


    

