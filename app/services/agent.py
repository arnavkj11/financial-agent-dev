from typing import TypedDict, Literal, Annotated
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import ToolNode

from app.core.config import settings
from app.services.tools import run_sql_query, search_vector_db, get_db_schema, check_budget_status, diagnose_spending

# 1. Tools for LangChain
@tool
async def query_sql_tool(query: str):
    """
    Run a SQL query. The table name is 'transactions'.
    Columns: date, merchant, amount, category.
    Example: SELECT sum(amount) FROM transactions WHERE category = 'Food'
    """
    return await run_sql_query(query)

@tool
def vector_search_tool(query: str):
    """
    Search for transactions by semantic meaning.
    Example: "coffee shops" -> returns Starbucks, Dunkin transactions.
    """
    return search_vector_db(query)

@tool
async def budget_tool():
    """
    Check the status of budgets (Spending vs Limit).
    Use this when the user asks about "budgets", "limits", or "overspending".
    """
    return await check_budget_status()

@tool
async def diagnostics_tool():
    """
    Analyzes spending history to find patterns, subscriptions, and bad habits.
    Use this when user asks "Where can I save?", "Analyze my spending", or "Find subscriptions".
    """
    return await diagnose_spending()

# 2. State
class AgentState(TypedDict):
    # The 'add_messages' reducer ensures valid history is preserved
    messages: Annotated[list, add_messages]

# 3. Nodes (Brain)
def agent_node(state: AgentState):
    """
    The Brain. Decides which tool to call.
    """
    messages = state["messages"]
    
    # System Prompt with Schema Context
    schema = get_db_schema()
    system_message = SystemMessage(content=f"""
    You are a Financial Advisor. You have access to a SQL Database, Vector Store, and Diagnostic Tools.
    
    DATABASE SCHEMA:
    {schema}
    
    GUIDELINES:
    1. For aggregation (Total spent, Count, Average), write a SQL query and use 'query_sql_tool'.
    2. For searching specific items (Where did I eat?, Shopping), use 'vector_search_tool'.
    3. For budget checks, use 'budget_tool'.
    4. For ADVICE, SAVING TIPS, or SPENDING PATTERNS, use 'diagnostics_tool'.
    5. Always answer in a helpful, concise manner.
    """)
    
    # Combine system message with history. 
    # Ensure system message is first IF not already present (simplification)
    if not isinstance(messages[0], SystemMessage):
        messages = [system_message] + messages
    
    llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools([query_sql_tool, vector_search_tool, budget_tool, diagnostics_tool])
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "__end__"

# 4. Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode([query_sql_tool, vector_search_tool, budget_tool, diagnostics_tool]))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_graph = workflow.compile()
