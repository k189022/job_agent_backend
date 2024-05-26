import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.tasks.motivationLetterTask import MotivationLetterTask as Tasks
from src.agents.motivationLetterAgent import MotivationLetterAgent as Agents

# Load environment variables
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize agents and tasks
agents = Agents()
tasks = Tasks()

class MotivationLetterCrew:
    def __init__(self):
        # Initialize agents for the crew
        # self.cv_analyst_agent = agents.cv_analyst_agent()
        self.job_details = agents.job_details_agent()
        self.motivation_writer_agent = agents.motivation_letter_editor_agent()
        self.motivation_editor_agent = agents.motivation_letter_editor_agent()
        

    def crew(self, template, job_details, number, lebenslauf):
        """Creates the crew to handle all job application-related tasks"""
        # Initialize tasks
        # cv_analyst = tasks.cv_analyst_task(self.cv_analyst_agent, lebenslauf=lebenslauf)
        job_details = tasks.job_details(self.job_details, job_details= job_details)
        motivation_writer = tasks.motivation_letter_writter_task(self.motivation_writer_agent, template=template, cv_details=lebenslauf)
        motivation_editor = tasks.motivation_letter_editor_task(self.motivation_editor_agent, number=number)

        # Set the context of the task
        motivation_writer.context = [job_details]
        motivation_editor.context =[motivation_writer]

        return Crew(
            agents=[self.motivation_editor_agent, self.motivation_writer_agent],
            tasks=[motivation_writer, motivation_editor],
            process=Process.sequential,
            verbose=True

        )
