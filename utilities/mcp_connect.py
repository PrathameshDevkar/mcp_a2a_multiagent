# from mcp_discovery import MCPDiscovery
# from google.adk.tools.mcp_tool import MCPToolset
# from google.adk.tools.mcp_tool import StdioConnectionParams
# from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

# from mcp import StdioServerParameters
# #this will discover the mcp servers from config file and list out the 
# #server tools nad cache them as mcp tool set instances for adk agent
# class MCPConnect:
    
#     def __init__(self, config_file:str = ""):
#         self.discovery = MCPDiscovery(config_file = config_file)
#         self.tools : list[MCPToolset] =[]
#         self._load_all_tools()
        
    
#     async def _load_all_tools(self):
#         """loads all tools from the discovered mcp server"""
        
#         tools=[]
#         for name,server in self.discovery.list_servers():
#             if server.get("command") == "streamable_http":
#                 conn = StreamableHTTPServerParams(url = server['args'][0])
#             else:
#                 conn = StdioConnectionParams(
#                     server_params = StdioServerParameters(
#                         command = server["command"],
#                         args = server["args"]
#                     )
#                 )
#             toolset = MCPToolset(connection_params = conn)
#             tool_set = await toolset.get_tools()
            
#             tool_names = [tool.name for tool in tool_set]
#             print("tool_names are", tool_names)
            
#             tools.append(toolset)
            
#         return tools
        
        
from mcp_discovery import MCPDiscovery 
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from mcp import StdioServerParameters

class MCPConnect:
    
    def __init__(self,config_file:str =""):
        self.config_file = MCPDiscovery(config_file=config_file)
        self.tools : list[MCPToolset] = []
        
    async def _load_all_tools(self):
        
        for name,server in self.config_file.list_servers():
            if server.get("command") == "streamable_http":
                conn = StreamableHTTPServerParams(url = server["args"][0])
            else:
                conn = StdioConnectionParams(
                    server_params = StdioServerParameters(
                        command = server["command"],
                        args = server["args"]
                    )
                )
                tools = MCPToolset(connection = conn)
                tool_set = await tools.get_tools()
                
                self.tools.append(tools)