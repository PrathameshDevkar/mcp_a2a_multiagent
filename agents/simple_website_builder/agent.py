from mcp_a2a_multiagent.utilities.common.file_loader import load_instructions_file
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from collections.abc import AsyncIterable
from google.genai import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Prathamesh\prathamesh\ai_agent\vertexai-free-credits-api-key.json"
vertexai.init(project = "poised-cortex-462609-n4", location = "us-central1")

# model = GenerativeModel("gemini-2.5-flash")
model = "gemini-2.5-flash"

instructions_file_path = r"C:\Users\Prathamesh\prathamesh\ai_agent\mcp_a2a_multiagent\agents\simple_website_builder\instructions.txt"
descriptions_file_path = r"C:\Users\Prathamesh\prathamesh\ai_agent\mcp_a2a_multiagent\agents\simple_website_builder\description.txt"

class simpleWebsiteBuilder:
    """
    A simpler website builder agent that can create basic web pages and
    is built using google's agent development kit 
    """

    def __init__(self):
        self.SYSTEM_INSTRUCTIONS = load_instructions_file(instructions_file_path)
        self.DESCRIPTIONS = load_instructions_file(descriptions_file_path)
        self._agent = self._build_agent()
        self._user_id = "website_builder_simple_agent_user"
        self._runner = Runner(
            app_name = self._agent.name,
            agent= self._agent,
            artifact_service = InMemoryArtifactService(),
            session_service = InMemorySessionService(),
            memory_service = InMemoryMemoryService()
        )

    def _build_agent(self) -> LlmAgent:
        return LlmAgent(
            name = "simple_website_builder",
            model= model ,
            instruction = self.SYSTEM_INSTRUCTIONS,
            description = self.DESCRIPTIONS,
        )
    
    async def invoke(self, query:str, session_id: str) -> AsyncIterable[dict]:
        """
        Invoke the agent
        Return a stream of updates back to the caller as the agent processes the query

        {
            'is_task_complete':bool, #Indicates if the task is complete
            'updates': str, #Updates on the task progress
            'content': str, #Final result if the task is complete
        }
        """

        session= await self._runner.session_service.get_session(
            app_name = self._agent.name,
            session_id = session_id,
            user_id = self._user_id
        )

        if not session:
            session = self._runner.session_service.create_session(
                app_name = self._agent.name,
                session_id = session_id,
                user_id = self._user_id
            )

        #the message to be send to adk has to be certian format and
        # this will achieve by the google.genai "types".
        user_content = types.content(
            role = "user",
            parts = [types.Part.from_text(text = query )]
        )

        #below is what will run the agent and get the streamed output
        # to catch the streaming output use 'for'
        async for event in self._runner.run_async(
            user_id = self._user_id,
            session_id = session_id,
            new_message = user_content
        ):
            if event.is_final_response:
                final_response=""
                if event.content and event.content.parts and event.content.parts[-1].text:
                    final_response = event.content.parts[-1].text

                    #this yield will return to the caller
                    yield {
                        "is_task_complete": True,
                        "content": final_response
                    }
            else:
                yield {
                    "is_task_complete":False,
                    "updates": "Agent is processing your task..." 
                }
