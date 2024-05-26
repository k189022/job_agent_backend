from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends
from endpoints.supabase_clients import get_supabase_user
from crew import run_agent  # Ensure this imports the correct asynchronous version

agent_router = APIRouter()

@agent_router.post("/run_agent", status_code=200)
async def run_agent_endpoint(background_tasks: BackgroundTasks, user_id:str = Depends(get_supabase_user)):
    background_tasks.add_task(run_agent(user_id = user_id))
    return {"message": "Agent run successfully"}
