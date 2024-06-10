import asyncio
import json
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from src.crews.jobSearchCrew import JobCrew
from src.crews.motivationLetterCrew import MotivationLetterCrew
from src.utils.fileManagement import FileManagement
from src.utils.data import Data
from src.monggoDB.models.motivationLetter import MotivationLetterModel

load_dotenv()

async def run_agent(user_id):
    print("Kick off run")
    lebenslauf_file = PyPDFLoader("./src/data/kuantanu.pdf")
    lebenslauf = lebenslauf_file.load_and_split()
    # template = FileManagement.file_read("./data/template.md")

    # JobCrew().crew(lebenslauf=lebenslauf, user_id=user_id).kickoff()


    
    job_file_path = './src/'
    job_urls = FileManagement.read_all_json_from_folder(job_file_path)

    print("Run is running")
    print (job)
    for job in job_urls:
        await Data.post(json=job, user_id=user_id)




async def run_motlet(user_id, job):

    template = await Data.get_template(user_id= user_id)


    cv_file_path = './cv_summary.md'
    cv_details = FileManagement.file_read(cv_file_path)


    


    MotivationLetterCrew().crew(job_details=job.url, template=template, lebenslauf=cv_details, user_id=user_id, job_id=job.id).kickoff()

    job_path = './motivation_letter.md'

    letter = FileManagement.file_read(job_path)

    letter_list = MotivationLetterModel(
        user_id=user_id,
        job_id=job.id,
        company= job.company,
        content=letter
    )


    Data.post_motlet(letter=letter_list)