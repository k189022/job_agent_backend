from textwrap import dedent
from src.tools.exa_tools import ExaSearchToolset
from src.tools.search_tools import SearchTools
from crewai import Agent
import os
from dotenv import load_dotenv

from src.tools.tools import Tools


load_dotenv()


openai_api_key=os.getenv("OPENAI_API_KEY")


class JobSearchAgent:

    def cv_analyst_agent(self):
        return Agent(
            role='CV Analyst',
            goal= "Analyze and summarize CVs, recommending potential job types based on the applicant's experience.",
            backstory=dedent("""\
                As a seasoned career advisor, you have a keen ability to dissect and understand the intricacies of complex curricula vitae (CVs). 
                Your expertise allows you to accurately extract and summarize essential skills, 
                job experiences, and educational backgrounds. Armed with this analysis, 
                you adeptly recommend career paths that best suit each candidate's unique qualifications and professional aspirations."""),
            memory=True,
            # llm=llm,
            allow_delegation=False,
            verbose=True

        )
    
    def job_position_agent(self):
        return Agent(
            role='Analyze the summary recent work experience and skills from the CV and Identify 2 or 3 job titles candidate might be looking for.',
            goal='based on his recent woork experience and skills determine the 2 or 3 job titles the person is suitable applying for.',
            backstory=dedent("""\
                You excel at analyzing the summary of work experience and skills and Identifying the job titles that are most suitable for 
                the candidate. Please make sure to pay extra attention to the recent work experiences and title of the most recent job. 
            """),
            memory=False, 
            # tools=ExaSearchToolset.tools_job_search(),
            allow_delegation=False,
            verbose=True
        )


    def job_search_agent(self):
        return Agent(
            role='Job Researcher',
            goal="Identify and summarize job openings in Germany from glassdoor that closely match the candidate's profile and the job titles",
            backstory=dedent("""\
                You excel in navigating the complex job market, adept at pinpointing and summarizing relevant job opportunities. 
                Your expertise lies in matching these opportunities with candidate profiles meticulously, focusing on perfect job for the candidate"""),
            memory=True,
            # tools=ExaSearchToolset.tools_job_search(),
            # tools=[SearchTools.open_page, SearchTools.search_internet],
            tools=[Tools.search_tool],
            verbose=True
        )
    
    def glassdoor_scrapper_agent(self):
        return Agent(
            role='Glassdoor scrapper',
            goal="Identify and summarize job openings from glassdoor based on job search given url.",
            backstory=dedent("""\
                You excel in navigating the complex job market, adept at pinpointing and summarizing relevant job opportunities. 
                Your expertise lies in matching these opportunities with candidate profiles meticulously, focusing on delivering 
                a curated list high-quality job openings."""),
            memory=True,
            allow_delegation=False,
            # tools=ExaSearchToolset.tools_job_search(),
            # tools=[SearchTools.open_page, SearchTools.search_internet],
            tools=[Tools.glassdoor_tool],
            verbose=True
        )