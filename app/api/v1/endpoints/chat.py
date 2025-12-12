from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.services.agent import app_graph
from app.api.deps import get_current_user
from app.models.sql import User

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/message", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Interact with the Financial Agent.
    """
    try:
        # Invoke the LangGraph agent
        # The input is the initial state: a list of messages
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # We use .invoke() to run the graph until the end
        result = await app_graph.ainvoke(inputs)
        
        # Extract the last message content (the agent's final answer)
        last_message = result["messages"][-1]
        
        return ChatResponse(response=last_message.content)
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
