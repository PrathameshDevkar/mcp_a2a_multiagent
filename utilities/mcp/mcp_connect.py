from __future__ import annotations

import logging

from mcp_a2a_multiagent.utilities.mcp.mcp_discovery import MCPDiscovery
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from mcp import StdioServerParameters

logger = logging.getLogger(__name__)

class MCPConnector:
    """
    Discovers the mcp servers from the config.
    then the config will be loaded by the MCP discovery class
    Then it list out the mcp server tools.
    Then caches those tools as MCPToolset so they are compatible with google's agent development kit.
    """

    def __init__(self, config_file: str = None):
        self.discovery = MCPDiscovery(config_file)
        self._toolsets: list[MCPToolset] = []
        self._initialized = False

    async def get_toolsets(self)-> list[MCPToolset]:
        """
        Returns all MCPToolsets.

        MCPToolset creted only once.
        """

        if not self._initialized:
            await self._load_all_toolsets()

        return self._toolsets

    async def _load_all_toolsets(self) -> None:
        for name, server in self.discovery.list_servers().items():
            try:
                if server.get("command")== "streamable_http":
                    conn = StreamableHTTPServerParams(url = server["args"][0])
                
                else:
                    conn = StdioConnectionParams(
                        server_params = StdioServerParameters(
                            command = server["command"],
                            args = server["args"]
                        ),
                        timeout =5
                    )

                toolset = MCPToolset(connection_params = conn)
                tools = await toolset.get_tools()

                logger.info(
                    "Discovered %d tools from '%s': %s ",
                    len(tools),
                    name,
                    [tool.name for tool in tools]
                )

                self._toolsets.append(toolset)
            
            except Exception:
                logger.exception(
                    "Failed to initilaize the MCP server: '%s'",
                    name
                )
        self._initialized=True


"""
Your MCPConnector creates an MCPToolset, which acts as the MCP client.

When you eventually do something like:

toolset = MCPToolset(connection_params=conn)
tools = await toolset.get_tools()

the client library performs the entire handshake automatically before asking the server for its tool list.

So although your code doesn't explicitly send initialize or notifications/initialized, those protocol messages are still being exchanged behind the scenes.


the MCPToolset is responsible for:

Establishing the connection to the server.
Performing the initialization handshake we discussed earlier.
Discovering available tools with tools/list.
Later, when an agent selects add_number, constructing the tools/call JSON-RPC request exactly as we've traced.
Receiving the response and presenting it back to the ADK agent as a normal tool result.





MCPToolset.get_tools()

        │
        ▼
Connect to server

        │
        ▼
initialize

        │
        ▼
notifications/initialized

        │
        ▼
tools/list

        │
        ▼
Receive tool metadata

        │
        ▼
Create ADK Tool objects

        │
        ▼
Return tools

"""


