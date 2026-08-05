"""
as we are using teh RemoteA2AAgent of teh adk and it does the work of this agent_connect file we wont ne needing this file
"""










# from typing import Dict
# from dataclasses import dataclass
# import logging
# import uuid

# from a2a.client import ClientConfig
# from a2a.types import (
#     AgentCard,
#     Message,
#     Part,
#     Role,
#     SendMessageRequest
#     ) 
# from a2a.client import Client, ClientConfig, create_client

# from mcp_a2a_multiagent.utilities.a2a.agent_discovery import AgentDiscovery


# logger = logging.getLogger(__name__)

# class AgentNotFoundError(Exception):
#     """Raised when a requested remote agent is not available"""

# @dataclass
# class RemoteAgent:
#     card: AgentCard
#     client: Client

# class AgentConnector:
#     """
#     Responsible for managing connections to a2a agents.

#     Responsibilities:
#     1. Discover available agents
#     2. Create A2A clients
#     3. Cache AgentCards
#     4. Cache connected clients
#     5. Provide a simple API for sending messages to remote agents
#     """

#     def __init__(self, registry_file: str | None = None, client_config: ClientConfig | None = None) -> None:
#         """
#         Initialize the connector

#         Parameters:
#             resgistry_file :str = path to the agent_registry.json file
#             client_ocnfig: ClientConfig = Optional A2A Client configuration. If None, the sdk default configuration will be used
#         """

#         self.discovery = AgentDiscovery(registry_file)
#         self.client_config = client_config or ClientConfig()
#         self.agents : Dict[str, RemoteAgent] = {}

#     async def initialize(self) -> None:
#         """
#         Initialize the connector.
        
#         This method performs all asynchronous initialization. Must be called before using the connector
#         """
#         await self._load_all_agents()

#     async def _load_all_agents(self) -> None:
#         """
#         Discover every registered agent and create a reusable A2A client for each one.
#         This methos is called only once during the initialize().
#         """

#         logger.info("Discovering remote A2A agents")

#         try:
#             agent_cards = await self.discovery.list_agent_cards()
#             logger.info(
#                 "Discovered %d agent(s)",
#                 len(agent_cards)
#             )

#             for card in agent_cards:
#                 try: 
#                     client = await create_client(
#                         agent = card,
#                         client_config = self.client_config
#                     )

#                     self.agents[card.name] = RemoteAgent(card = card, client = client)

#                     logger.info(
#                         "Connected to agent: %s",
#                         card.name
#                     )
                
#                 except Exception as e:
#                     logger.exception(
#                         "Failed to connect to agent '%s': %s",
#                         card.name,
#                         str(e)
#                     )
        
#         except Exception as e:
#             logger.exception(
#                 "Agent discovery failed: %s",
#                 str(e)
#             )

#     def list_agents(self) -> list[dict]:
#         """
#         Return lightweight summary of every discovered agent.

#         This method intentionally hides the underlying AgentCard and client implementations.
#         """

#         agents = []

#         for remote_agent in self.agents.values():
#             card = remote_agent.card

#             agents.append(
#                 {
#                     "name": card.name,
#                     "description":card.description,
#                     "version":card.version,
#                     "skill":[
#                         {
#                             "id": skill.id,
#                             "name":skill.name,
#                             "description":skill.description,
#                             "examples":list(skill.examples)
#                         }
#                         for skill in card.skills
#                     ]
#                 }

#             )
        
#         return agents
    
#     def get_agent(self, agent_name:str) -> RemoteAgent:
#         """
#         Returns the cacehd A2A client for the remote agent.

#         Parameters:
#             agent_name: Name of the remote agent
        
#         returns:
#             RemoteAgent: remote agent class object containing agent card and client

#         raises AgentNotFoundError if the requested agent does not exist

#         """

#         remote_agent = self.agents.get(agent_name)

#         if remote_agent is None:
#             available = ", ".join(sorted(self.agents.keys()))

#             raise AgentNotFoundError(
#                 f"Remote agent {agent_name} not found.\n"
#                 f"Available agents are: {available}"
#             )
        
#         return remote_agent

#     async def send_message(
#         self,
#         agent_name: str,
#         message: str,
#         task_id: str | None,
#         context_id: str | None
#     ):
#         """
#         Send message to the remote agent.

#         This method is implemented as an async generator, 
#         allowing caller to stream teh output as it arrives.
#         """

#         remote_agent = self.get_agent(agent_name)
#         client = remote_agent.client

#         request = SendMessageRequest(
#             message = Message(
#                 role = Role.ROLE_USER,
#                 message_id = str(uuid.uuid4()),
#                 parts = [
#                     Part(text = message)
#                 ],
#                 task_id = task_id,
#                 context_id = context_id or str(uuid.uuid4())
#             )
#         )

#         stream = client.send_message(request)

#         async for event in stream:
#             yield event
