import os
from typing import Dict, Any
import json

class MCPDiscovery:
    def __init__(self, config_file: str = None):
        """
        Initialize mcp discovery with a configuration file.
        if None defaults to 'mcp_config.json' located in the
        same directory as this module.
        """
        if config_file is None:
            self.config_file = os.path.join(os.path.dirname(__file__), "mcp_config.json")
        
        else:
            self.config_file = config_file
        
        self.config = self._load_config()

    def _load_config(self) -> Dict[str,Any]:
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError(f"Invalid configuration format in {self.config_file}")

            return data
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except Exception as e:
            raise RuntimeError(f"Errorreading configuration file {self.config_file}: {str(e)}")

    def list_servers(self)-> Dict[str,Any]:
        """
        Returns the mcp servers defined in the config file.

        Returns:
            Dict[str, Any]: The content of the 'mcpservers' key from the config.

        raise:
            KeyError: raises error if mcpServers key not found in the configuration.
        """
        if "mcpServers" not in self.config:
            raise KeyError(f"mcpServers key not found in {self.config_file}")
        
        return self.config['mcpServers']

