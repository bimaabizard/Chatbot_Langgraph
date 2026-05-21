import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.redis import RedisSaver
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from app.tools import agent_tools
from app.utils import setup_enterprise_logger
from app.tools import retrieve_corporate_data # Hypothetical tool

# 1. Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context_retrieved: bool

# 2. Node Functions
def call_model(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o")
    # Bind tools here if needed
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# 4. Redis Persistence Setup
REDIS_URI = os.getenv("REDIS_URL", "redis://localhost:6379")

def get_compiled_graph():
    """
    Returns the compiled graph with the Redis checkpointer attached.
    In a real app, manage the Redis connection lifecycle carefully.
    """
    # Using RedisSaver for production-grade thread-level memory
    checkpointer = RedisSaver.from_conn_string(REDIS_URI)
    checkpointer.setup() # Initializes necessary Redis indices
    
    return workflow.compile(checkpointer=checkpointer)

# Add these imports at the top of app/agent.py

logger = setup_enterprise_logger("agent_workflow")

# Inside your call_model function, bind the tools:
def call_model(state: AgentState):
    logger.info(f"Invoking LLM for thread state with {len(state['messages'])} messages.")
    llm = ChatOpenAI(model="gpt-4o")
    
    # Bind the tools from tools.py to the LLM
    llm_with_tools = llm.bind_tools(agent_tools)
    
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# You will also need to add the ToolNode to your graph in agent.py
# workflow.add_node("tools", ToolNode(agent_tools))