import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.tasks.jobSearchTask import JobSearchTask as Tasks
from src.agents.jobSearchAgent import JobSearchAgent as Agents

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize agents and tasks
agents = Agents()
tasks = Tasks()

class JobCrew:
    def __init__(self):
        self.cv_analyst_agent = agents.cv_analyst_agent()
        self.job_title_agent = agents.job_position_agent()
        self.job_search_agent = agents.job_search_agent()
        self.glassdoor_scrapper = agents.glassdoor_scrapper_agent()

    def crew(self, lebenslauf, user_id):
        """Creates the crew to handle all job application-related tasks"""

        cv_analyst = tasks.cv_analyst_task(self.cv_analyst_agent, lebenslauf=lebenslauf)
        job_titles = tasks.job_title_task(self.job_title_agent) 
        job_research = tasks.job_search_task(self.job_search_agent)
        glassdoor_scrapper = tasks.glassdoor_scrapper_task(self.glassdoor_scrapper, user_id=user_id)

        # Set up context dependencies
        job_titles.context = [cv_analyst]
        job_research.context = [job_titles]
        glassdoor_scrapper.context = [job_research]


        return Crew(
            agents=[self.cv_analyst_agent, self.job_title_agent, self.job_search_agent, self.glassdoor_scrapper],
            tasks=[cv_analyst, job_titles, job_research, glassdoor_scrapper],
            verbose=2,
            process=Process.sequential
        )
