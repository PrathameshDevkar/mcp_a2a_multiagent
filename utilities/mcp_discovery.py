
# purpose - to lead the json config file of the mcp nad provide access to the mcp server definitions
import json
from typing import Any

class MCPDiscovery:
    """
    reads a json config file definig the mcp servers and 
    provide access to the server definition under the mcpservers key
    
    attributes:
    config_file(str): path to the json config file.
    config(Dict[str,Any]): Parsed JSON content, expected to contain mcpservers key.
    
    
    """
    def __init__(self,config_file:str=""):
        """
        initialize the mcp discovery with the configuration file.
        """
        self.config_file = config_file
        self.config = self._load_config()
        
        
    def _load_config(self) -> dict[str,Any] :
        with open(self.config_file, "r") as f:
            data = json.load(f)
            
        return data
    
    def list_servers(self):
        return self.config.get("mcpServers",{})
    
# import json
# from typing import Any
# class MCPDiscovery:
    
#     """reads the json file definnig mcp server and
#     provide access to the server definition"""

#     def __init__(self, config_file:str=""):
#         """
        
#         """
#         self.config_file = config_file
#         self.config = self._load_config()  
        
#     def _load_config(self) -> dict[str, Any] :
#         with open(self.config_file, "r") as f:
#             data = json.load(f)
            
#         return data
    
#     def list_servers(self):
        
#         return self.config.get("mcpservers",{})
          