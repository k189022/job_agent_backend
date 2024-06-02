from crewai import Task
from textwrap import dedent
from src.config.schema import JobList
from src.tools.exa_tools import ExaSearchToolset

class JobSearchTask:

    def cv_analyst_task(self, agent, lebenslauf):
        return Task(
            description=dedent(f"""\
                    Read the CV content from {lebenslauf} and analyze the provided CV by reviewing the document carefully. 
                    Examine the document thoroughly to gather information about the individual's skills, job experiences, 
                    and educational background. Summarize these details succinctly in preparation for drafting a motivation letter. 
                    Ensure all information from the CV is captured accurately without redundancy. Focus on presenting a clear, 
                    fact-based summary of the qualifications."""),
            expected_output= dedent("""\
                    Summerise about the candidate, list of skills, list academic background, list work experience"""),
            agent = agent,
            output_file = "cv_summary.md"
        )
    
    def job_title_task(self, agent):
        return Task(
            description=dedent("""\
                Your task is to analyze the summary of recent work experience and skills and Identify 2 or 3 job titles that are most 
                suitable for the candidate from the CV.  
            """),
            expected_output=dedent("""\
                Your are expected to generate a list of job titles based on the recent work experience and job titles. Make sure that the 
                output you generate is a valid python list. 
            """),
            agent=agent
        ) 

    def job_search_task(self, agent):
        return Task(
            description=dedent(f"""\
                    Search in google the relevat job based on the candidate's profile and the job titel in linkedIn
                    Do not make up anything, just give the result based on search engine
                    chose maximum 3 url that closest to the job titel as the output"""),
            expected_output=dedent("""\
                    Maximum 3 list of URL and job title of the job"""),
            agent=agent,
        )
    
    def glassdoor_scrapper_task(self, agent, user_id):
        return Task(
            description=dedent("""\
                    Use the scrapper tools to get the list of the open job for each url from `job search` as the query.
                    chose css tag wisely, that you can the list of the jobs.
                    If you get more than one recomendation url, Pass one by one of url.
                    Do not make up anything, give the result based on the list of the given website."""),
            expected_output=dedent("""\
                    The list of relevant job that allign with the job title"""),
            agent=agent,
            output_json=JobList,
            # tools = ExaSearchToolset.tools_get_details(),
            output_file= "job.json"
        )
    
