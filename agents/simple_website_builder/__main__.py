# This file will have two things - agent skills and agent card

from a2a.types import AgentSkill, AgentCard, AgentCapabilities, AgentInterface
import click
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from mcp_a2a_multiagent.agents.simple_website_builder.agent_executor import simpleWebsiteBuilderAgent

from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes

from fastapi import FastAPI
import uvicorn

#to make the main function as command line interface use click
"""
The script uses the click library to transform a standard Python function into a formal command-line tool. This lets you start your agent server from the terminal while flexibly 
overriding host names and port assignments (defaulting to localhost:3001).
"""
@click.command()
@click.option('--host', default='localhost', help='host for the agent server')
@click.option('--port', default=3001, help='port for the agent server')
def main(host:str, port:int):

    """main function to create and run the website builder agent"""

    """
    AgentSkill: Think of this as the agent's resume entry. In an A2A ecosystem, routers or other agents need to know what tasks to delegate. 
    By explicitly declaring its description, tags, and semantic execution examples, the overarching framework can dynamically match user prompts to this specific agent.
"""
    skill = AgentSkill(
        id = "website_builder_simple_skill",
        name = "website_builder_simple_skill",
        description = "A simple website builder agent that can create basic web pages",
        tags = ["website", "builder","html","css","javascript"],
        examples = [
            """Create a simple web page with a header and footer.""",
            """Create a landing page for a product with call to actin button. """
        ]
    )

    """
    AgentCard: This acts as the public manifest or identity card for the agent service. 
    It tells the network where the agent lives (url), its current semantic layout (version), its valid input/output data forms (text), and that it supports real-time data streaming
    """
    agent_card = AgentCard(
        name = "simple_website_builder",
        description = "This agent takes single query for a website and generated single self-contained HTML file with embedded CSS and javascript.",
        supported_interfaces = [
            AgentInterface(
                protocol_binding = "JSONRPC",
                url = "http://localhost:3001/a2a/jsonrpc/" #this does not create /a2a/jsonrpc, it only tells other agents that 'if you want to talk to me using JSON-rpc, connect here'.
            )
        ],
        version = "1.0.0",
        default_input_modes = ["text"],
        default_output_modes = ["text"],
        skills = [skill],
        capabilities = AgentCapabilities(streaming = True)
    )

    request_handler = DefaultRequestHandler(
        agent_executor = simpleWebsiteBuilderAgent(),
        task_store = InMemoryTaskStore(),
        agent_card = agent_card
    )

    routes=[]
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, rpc_url = "/a2a/jsonrpc/")) # this actually builds the api route for the fastapi to use.
    
    app = FastAPI(routes = routes)

    uvicorn.run(app, host = host, port = port)

if __name__ == "__main__":
    main() 