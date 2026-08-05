from contextlib import asynccontextmanager

from fastapi import FastAPI


from mcp_a2a_multiagent.application.controllers.chat_controller import router as chat_router
from mcp_a2a_multiagent.application.services.chat_service import ChatService
from mcp_a2a_multiagent.application.runtime.host_runtime import HostRunTime

from mcp_a2a_multiagent.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/ shutdown.
    """
    app_name = settings.APP_NAME
    model = settings.MODEL
    mcp_config_path = settings.MCP_CONFIG_PATH
    agent_registry_path = settings.A2A_REGISTRY_PATH

    runtime = HostRunTime(
        app_name = app_name,
        model = model,
        mcp_config_path = mcp_config_path,
        agent_registry_path = agent_registry_path
    )

    await runtime.initialize()

    app.state.runtime = runtime
    app.state.chat_service = ChatService(runtime)

    yield

    await runtime.shutdown()

app = FastAPI(
    title = "Multi-Agent Platform",
    version = "1.0.0",
    lifespan = lifespan
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "healthy"}