# from mcp.server.fastmcp import FastMCP
# from pydantic import BaseModel, Field

# class ArithematicInput(BaseModel):
#     a : float =Field(description = "first number")
#     b: float=Field(description = "second number")

# class ArithematicOutput(BaseModel):
#     result: float = Field(description = "result of the arithematic operation")
#     expression : str = Field(description = "expression evaluator")
    
# mcp = FastMCP(
#     "arithematic_server",
#     host = "localhost",
#     port = 3000,
#     stateless_http=True,
# )

# #stateless_http=True := the events and communcations wont persist accross the process and even in the same session

# @mcp.tool("add_number")
# async def add_numbers(input:ArithematicInput) -> ArithematicOutput :
#     """
#     Add two numbers and return the result
#     args:
    
#     return:
    
    
#     """
#     result = input.a + input.b
#     expression = f"{input.a} + {input.b} = {result}"
#     return ArithematicOutput(result=result, expression=expression)

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

class arithematicInput(BaseModel):
    a:float =  Field(description = "first number")
    b:float = Field(description = "second number")

class arithematicOutput(BaseModel):
    result: float=Field(description = "result of the arithematic calculation")
    expression: str = Field(description = "expression evaluator")

mcp = FastMCP(
    "arithematic_server",
    host = "localhost",
    port = 3000,
    stateless_http = True
)

@mcp.tool("add_numbers")
async def add_number(input:arithematicInput) -> arithematicOutput:
    result = input.a+input.b
    expression = f"{input.a} + {input.b} = {result}"
    return arithematicOutput(result = result, expression = expression)

if __name__ == "__main__":
    mcp.run(transport = "streamable-http")

