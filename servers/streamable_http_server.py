from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

class ArithematicInput(BaseModel):
    a : float =Field(description = "first number")
    b: float=Field(description = "second number")

class ArithematicOutput(BaseModel):
    result: float = Field(description = "result of the arithematic operation")
    expression : str = Field(description = "expression evaluator")
    
mcp = FastMCP(
    "arithematic_server",
    host = "localhost",
    port = 3000,
    stateless_http=True,
)

#stateless_http=True := the events and communcations wont persist accross the process and even in the same session

@mcp.tool("add_number")
async def add_numbers(input:ArithematicInput) -> ArithematicOutput :
    """
    Add two numbers and return the result
    args:
    
    return:
    
    
    """
    result = input.a + input.b
    expression = f"{input.a} + {input.b} = {result}"
    return ArithematicOutput(result=result, expression=expression)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

"""
How this relates to your code

Take your arithmetic server:

mcp = FastMCP(
    "arithematic_server",
    host="localhost",
    port=3000,
    stateless_http=True,
)

and then:

@mcp.tool("add_number")

When you call:

mcp.run(transport="streamable-http")

FastMCP is doing much more than just starting an HTTP server.

Internally, it:

Starts listening for incoming MCP connections.
Waits for an initialize request.
Validates the protocol version and client capabilities.
Sends back its own server information and capabilities.
Waits for the notifications/initialized message.
Only then allows requests like tools/list and tools/call.

All of this handshake logic is handled by the framework, which is why your application code only needs to register tools.

"""