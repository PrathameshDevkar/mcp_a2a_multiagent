"""
bridge file between agent and a2a framework. this file will contain two functions-
execute and cancel that will help connect this agent to a2a framwork


The AgentExecutor is the adapter that allows the A2A framework to invoke any Python agent without needing to know how that agent is implemented.

The framework only knows two methods:

execute()
cancel()

It doesn't know whether your agent:

uses Google ADK,
uses LangGraph,
calls MCP servers,
talks to OpenAI,
or is just plain Python code.

As long as the AgentExecutor implements the expected interface, the framework can host it.

This separation is one of the biggest architectural strengths of A2A because it cleanly decouples the protocol layer (A2A) from the reasoning layer (your agent) and the capability layer (MCP tools). 
Once you internalize those three layers, you'll be able to design much more complex multi-agent systems without them becoming tightly coupled.
"""
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from mcp_a2a_multiagent.agents.simple_website_builder.agent import simpleWebsiteBuilder
from a2a.helpers.proto_helpers import new_task, new_task_from_user_message
from a2a.server.tasks import TaskUpdater
from a2a.types import(
    Task,
    TaskState,
    UnsupportedOperationError
)

import asyncio

class simpleWebsiteBuilderAgent(AgentExecutor):
    """
    Implements the agent executor interface to integrate the 
    simple website builder agent with A2A framwork
    """

    def __init__(self):
        self.agent = simpleWebsiteBuilder()
        
    async def execute(self, context: RequestContext, event_queue: EventQueue)-> None :
        """
        executes the agent with the provided context and event queue.
        """
        query = context.get_user_input()  #extracts the text content from the user's message parts.
        task = context.current_task     
        if not task:
            task= new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)   #this queue is going to hold this task and all the related updates of this task and give it back to the user

        updater = TaskUpdater(event_queue, task.id, task.contextId) #helper class for agents to publish upadtes to task's event queue
        #contextid - maintains contxt across multiple tasks

        try:

            async for item in self.agent.invoke(query, task.contextId):
                is_task_complete = item.get("is_task_complete", False)

                if not is_task_complete:
                    message = item.get('updates', 'The Agent is still working on your request.')
                    await updater.update_status(
                        TaskState.working,
                        message(message, task.contextId, task.id)
                    )

                else:
                    final_result = item.get('content', 'no result received')        
                    await updater.update_status(
                        TaskState.completed,
                        message(final_result, task.contextId, task.id)
                    )

                    await asyncio.sleep(0.1) #allow for the message to be processed

                    break

        except Exception as e:
            error_message = f"An error occured: {str(e)}"
            await updater.update_status(
                TaskState.failed, 
                message(error_message, task.id, task.contextId)
            )
            raise

    async def cancel(self, request:RequestContext, event_queue:EventQueue) -> Task | None:
        raise UnsupportedOperationError("Task cancellatiomn is not supported by the simplewebsitebuilderagent")
