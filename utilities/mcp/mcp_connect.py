from mcp_a2a_multiagent.utilities.mcp_discovery import MCPDiscovery
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from mcp import StdioServerParameters

class MCPConnector:
    """
    Discovers the mcp servers from the config.
    then the config will be loaded by the MCP discovery class
    Then it list out the mcp server tools.
    Then caches those tools as MCPToolset so they are compatible with google's agent development kit.
    """

    def __init__(self, config_file: str = None):
        self.discovery = MCPDiscovery(config_file)
        self.tools: list[MCPToolset] = []

    async def initialize(self):
        await self._load_all_tools()

    async def _load_all_tools(self):
        "list all the tools of the mcp server"
        try:
            for name, server in self.discovery.list_servers():
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

                tool_names = [tool.name for tool in tools]
                print("========tools are======", tool_names)

                self.tools.append(toolset)
        except Exception as e:
            print(f"error while connecting to the mcp server: {str(e)}")


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


