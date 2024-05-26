import asyncio
import json
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from src.crews.jobSearchCrew import JobCrew
from src.crews.motivationLetterCrew import MotivationLetterCrew
from src.utils.fileManagement import FileManagement
from src.utils.data import Data

load_dotenv()

async def run_agent(user_id):
    print("Kick off run")
    lebenslauf_file = PyPDFLoader("./src/data/kuantanu.pdf")
    lebenslauf = lebenslauf_file.load_and_split()
    # template = FileManagement.file_read("./data/template.md")

    url = "http://localhost:8000/job"



    cv_file_path = '.src/cv_summary.md'
    # cv_details = FileManagement.file_read(cv_file_path)

    JobCrew().crew(lebenslauf=lebenslauf).kickoff()

    
    job_file_path = './'
    job_urls = FileManagement.read_all_json_from_folder(job_file_path)
    job= job_urls[0]
    print (job)

    await Data.post(url, json=job, user_id=user_id)

    # num = 0
    # for job_url in job_urls:
    #     num +=1
    #     if num <= 1:
    #         await Data.post(url, json=job_url)
    #         print(job_url)


# import datetime
# # from job_crew import JobCrew
# from langchain_community.document_loaders import PyPDFLoader
# from dotenv import load_dotenv
# from crews.jobSearchCrew import JobCrew
# from crews.motivationLetterCrew import MotivationLetterCrew
# from utils.fileManagement import FileManagement
# from utils.data import Data





# load_dotenv()
# lebenslauf_file = PyPDFLoader("./data/kuantanu.pdf")
# lebenslauf = lebenslauf_file.load_and_split()
# template = FileManagement.file_read("./data/template.md")

# url = "http://localhost:8000/job"


# # Check for a successful request


# # job_list= Data.get(url)



# ### Job Crew
# # results = JobCrew().crew(lebenslauf=lebenslauf).kickoff()
# # print(results)



# job_file_path = './'
# job_urls = FileManagement.read_all_json_from_folder(job_file_path)


# # job_urls = "https://www.glassdoor.com/job-listing/data-scientist-in-mwd-remote-oder-karlsruhe-knuddels-gmbh-co-kg-JV_KO0,43_KE44,63.htm?jl=1007953941644"

# cv_file_path = './cv_summary.md'
# cv_details = FileManagement.file_read(cv_file_path)
# # print(cv_details)


# # print(job_urls)


# nums = 0
# for job_url in job_urls:

    
    
#     # nums+=1
#     # if (nums <2):
#     #     print(job_url)
#     # if(nums <= 5):
#     #     results = MotivationLetterCrew().crew(job_details=job_url, number=nums, template=template, lebenslauf=cv_details).kickoff()
#     #     print(results)

#     post = Data.post(url, json=job_url)

