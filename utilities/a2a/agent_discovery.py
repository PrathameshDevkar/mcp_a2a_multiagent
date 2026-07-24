import os
import json
from a2a.types import (
    AgentCard
)
import httpx
from a2a.client import A2ACardResolver, A2AClient


class AgentDiscovery:
    """
    Discovers A2A agents by reading a registry file of urls and 
    querying each one's ./well-known/agent.json file to retireve 
    an agent card

    Attributes:
        registry file path: (str) = Path to agent registry file
        base_urls: list[str] = list of base urls for a2a agents.
    """
    def __init__(self, registry_file: str):
        """
        Initialise the agent discovery.

        Arguments:
            registry_file: str = Path to agent_registry.json file. (defaults to 'utilities/a2a/agent_registry.json')
        """

        if registry_file:
            self.registry_file = registry_file
        else:
            self.registry_file = os.path.join(os.path.dirname(__file__), 'agent_registry.json')

        self.base_urls = self._load_registry()

    def _load_registry(self) -> list[str]:
        """
        reads the registry file and returns the list of urls in str format
        """
        try:
            with open(self.registry_file, "r") as f:
                data = json.laod(f)
            if not isinstance(data, list):
                raise ValueError("Registry file must contain list of urls")
            return data
        except FileNotFoundError:
            print(f"registry at {self.registry_file} not found")
            return []
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing registery file: {e}")
            return [] 

    # This method helps to return the list of agent cards
    async def list_agent_cards(self) -> list[AgentCard]:
        """
        Asynchronously fetches agent card from each base url in the registry.

        Returns:
            list[AgentCard] = list of AgentCards retrieved from agents.
        """

        cards: list[AgentCard] = []

        async with httpx.AsyncClient(timeout = 300.0) as httpx_client: #The timeout is 300 seconds to handle the long agent task
            for base_url in self.base_urls:
                resolver = A2ACardResolver(
                    base_url = base_url.rstrip('/'),
                    httpx_client = httpx_client
                )

                card = await resolver.get_agent_card()

                cards.append(card)

            return cards


