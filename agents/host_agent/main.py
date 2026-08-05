from __future__ import annotations

import asyncio
from pathlib import Path

from google.adk.agents import LlmAgent

from mcp_a2a_multiagent.agents.host_agent.agent import HostLlmAgent
from mcp_a2a_multiagent.config import settings

MCP_CONFIG_PATH= (
    Path(__file__).resolve().parents[2]
    / "utilities"
    / "mcp"
    / "mcp_config.json"
)

A2A_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "utilities"
    / "a2a"
    / "agent_registry.json"
)

async def create_root_agent() -> LlmAgent:
    """
    Building  the host agent.
    """
    builder= HostLlmAgent(
        model = settings.MODEL,
        mcp_config_path = MCP_CONFIG_PATH,
        agent_registry_path = A2A_REGISTRY_PATH
    )

    return await builder.build()

# ADK entry point
root_agent = asyncio.run(create_root_agent())