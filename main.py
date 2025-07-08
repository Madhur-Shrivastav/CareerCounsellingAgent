from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from root_agent.agent import root_agent
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

app = FastAPI()

APP_NAME = "Virtuon Customer Support"
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            state={
                "user_id": request.user_id,
            }
        )

        session_id = session.id

        await add_user_query_to_history(
            session_service, APP_NAME, request.user_id, session_id, request.message
        )

        response = await call_agent_async(runner, request.user_id, session_id, request.message)

        return {
            "session_id": session_id,
            "response": response,
            "state": session.state
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
