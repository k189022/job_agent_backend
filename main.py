from fastapi import FastAPI, Request
# from mySQL.config.db import engine
from fastapi.middleware.cors import CORSMiddleware
from routers.agent import agent_router as AgentRouter
from routers.monggo.user import user_router
from routers.monggo.job import job_router
from routers.monggo.motivation import motivation_letter_router
import sys
import os
# from mySQL.models import job as jobModel
# from mySQL.config.db import Base



# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI()
# jobModel.Base.metadata.create_all(engine)
# Base.metadata.create_all(engine)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     print(f"Request URL: {request.url}")
#     print(f"Request Headers: {request.headers}")
#     response = await call_next(request)
#     return response



app.include_router(AgentRouter, prefix='/agent')

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(motivation_letter_router, prefix="/motivation_letters", tags=["motivation_letters"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)



