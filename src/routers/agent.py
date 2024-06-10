from fastapi import APIRouter, BackgroundTasks, Body
from fastapi import Depends
from src.monggoDB.models.job import JobModel
from src.utils.supabase_clients import  get_supabase_user
from crew import run_agent, run_motlet  # Ensure this imports the correct asynchronous version

agent_router = APIRouter()

user_id ="75dcd09a-0264-4a3c-8a43-6871882f5ecf"

@agent_router.post("/run_agent", status_code=200)
async def run_agent_endpoint(user_id:str = Depends(get_supabase_user)):
# async def run_agent_endpoint(user_id:str = user_id):
    print(user_id)
    # async def run_agent_endpoint(background_tasks: BackgroundTasks, user_id:str = user_id):
    await run_agent(user_id=user_id)
    # background_tasks.add_task(run_agent(user_id = user_id))
    return {"message": "Agent run successfully"}

@agent_router.post("/createletter", status_code=200)
async def run_create_letter(job: JobModel = Body(...), user_id:str = Depends(get_supabase_user)):
# async def run_motlet(user_id:str = user_id, job: JobModel = Body(...)):
    
    # async def run_agent_endpoint(background_tasks: BackgroundTasks, user_id:str = user_id):
    await run_motlet(user_id=user_id, job=job)
    # import pdb;pdb.set_trace()
    # background_tasks.add_task(run_agent(user_id = user_id))
    return {"message": "Agent run successfully"}