import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from root_agent.agent import customer_support_agent
from utils import add_user_query_to_history, call_agent_async

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Set up the database-backed session service
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Runner instance for the agent
APP_NAME = "Virtuon Customer Support"
runner = Runner(
    agent=customer_support_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Pydantic model for incoming requests
class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_id = request.user_id
        user_input = request.message

        # Create or get session
        session = await session_service.get_or_create_session(
            app_name=APP_NAME,
            user_id=user_id,
            initial_state={
                "user_id": user_id,
                "user_name": "",
                "user_email": "",
                "orders": ""
            }
        )
        session_id = session.id

        # Log user query
        await add_user_query_to_history(session_service, APP_NAME, user_id, session_id, user_input)

        # Get agent response
        response = await call_agent_async(runner, user_id, session_id, user_input)

        # Return full updated state (or just agent reply)
        return {
            "session_id": session_id,
            "response": response,
            "state": session.state
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
