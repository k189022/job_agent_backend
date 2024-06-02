from typing import Optional
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import json
from src.utils.data import Data

class GlassdoorScraperTool(BaseTool):
    name: str = "GlassdoorScraperTool"
    description: str = "Scrapes job listings from a given Glassdoor URL."
    url:Optional[str]=None

    def __init__(self, url:Optional[str]=None):
        super().__init__()
        self.url = url


    def _run(self) -> str:
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.RequestException as e:
            return f"Failed to fetch content from {self.url}: {str(e)}"
        

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = soup.find_all("li", class_="JobsList_jobListItem__wjTHv")


            for job in job_listings:
                title_tag = job.find("a", class_="JobCard_jobTitle___7I6y")
                title = title_tag.text.strip() if title_tag else "Not provided"

                company_tag = job.find("span", class_="EmployerProfile_compactEmployerName__LE242")
                company = company_tag.text.strip() if company_tag else "Not provided"

                location_tag = job.find("div", class_="JobCard_location__rCz3x")
                location = location_tag.text.strip() if location_tag else "Not provided"

                description_div = job.find("div", class_="JobCard_jobDescriptionSnippet__yWW8q")
                description = description_div.text.strip() if description_div else "Not provided"

                skills = ""
                if "Skills:" in description:
                    parts = description.split("Skills:")
                    description = parts[0].strip()
                    skills = parts[1].strip()

                job_url_tag = job.find("a", class_="JobCard_trackingLink__GrRYn")
                job_url = job_url_tag['href'] if job_url_tag else "Not provided"
                full_url = f"https://www.glassdoor.com{job_url}" if job_url != "Not provided" else "Not provided"

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "skills": skills,
                    "url": full_url
                }

                Data.post(json=job_data, user_id="75dcd09a-0264-4a3c-8a43-6871882f5ecf")

            return f"Data successfully scraped and posted."
        
        else:
            return f"Failed to fetch content from {self.url}. HTTP Status Code: {response.status_code}"



