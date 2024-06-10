from crewai import Agent
from textwrap import dedent
from src.tools.tools import Tools
from dotenv import load_dotenv

load_dotenv()

class MotivationLetterAgent():
    
    # def cv_analyst_agent(self):
    #     return Agent(
    #         role='CV Analyst',
    #         goal="Analyze and summarize CVs, recommending potential job types based on the applicant's experience.",
    #         backstory=dedent("""\
    #             As a seasoned career advisor, you have a keen ability to dissect and understand the intricacies of complex curricula vitae (CVs). 
    #             Your expertise allows you to accurately extract and summarize essential skills, 
    #             job experiences, and educational backgrounds. Armed with this analysis, 
    #             you adeptly recommend career paths that best suit each candidate's unique qualifications and professional aspirations."""),
    #         # allow_delegation=False,
    #         # llm=llm,
    #         verbose=True
        # )

    def job_details_agent(self):
        return Agent(
            role='Job Summarizer',
            goal="Bullet point summarize the valuable details about the job",
            backstory=dedent("""\
                You excel in navigating the complex job market, adept at pinpointing and summarizing relevant infomation about specific job. 
                Your expertise lies in find valuable infomation from specific job posting, focusing on delivering 
                acurated linfomation on that job posting."""),
            # memory=True,
            # tools=ExaSearchToolset.tools_job_search(),
            # tools = [Tools.search_tool, Tools.scrape_tool],
            tools = [Tools.selenium_tool],
            verbose=True
        )
    
    def motivation_letter_writter_agent(self):
        return Agent(
            role='Motivation Letter Writer',
            goal="Craft tailored motivation letters that align with specific job details from job position and the applicant's qualifications.",
            backstory=dedent("""\
                Known for your eloquence and persuasive writing, 
                you specialize in creating bespoke motivation letters. 
                Each letter you craft is finely tuned to reflect the applicant’s skills and enthusiasm, 
                while also addressing the specific requirements and culture of the potential employer. 
                This meticulous approach ensures each application is compelling and distinct, 
                enhancing the applicant's chances in a competitive job market."""),
            verbose=True,
        )
    
    def motivation_letter_editor_agent(self):
        return Agent(
            role='Motivation Letter Editor',
            goal="Craft tailored motivation letters that align with specific job requirements and the applicant's qualifications.",
            backstory=dedent("""\
                With a sharp eye for detail and a flair for editing, 
                you transform standard motivation letters into personalized narratives 
                that convey an applicant’s qualifications and passion convincingly. 
                Your editing skills ensure each letter not only meets the job's specific demands 
                but also resonates with a human touch, making each application stand out 
                as authentically crafted by a thoughtful and insightful writer."""),
            verbose=True,
            allow_delegation=False,
        )
    
