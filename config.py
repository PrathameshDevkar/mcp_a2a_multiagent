from pydantic_settings import BaseSettings

class Settings():

    APP_NAME = "APP_v1"
    MODEL = "gemini-2.5-flash-lite"
    MCP_CONFIG_PATH = r"C:\Users\Prathamesh\prathamesh\ai_agent\mcp_a2a_multiagent\utilities\mcp\mcp_config.json"
    A2A_REGISTRY_PATH = r"C:\Users\Prathamesh\prathamesh\ai_agent\mcp_a2a_multiagent\utilities\a2a\agent_registry.json"


settings = Settings()
