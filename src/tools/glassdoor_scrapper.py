from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import json
from src.utils.data import Data

class GlassdoorScraperTool(BaseTool):
    name: str = "GlassdoorScraperTool"
    description: str = "Scrapes job listings from a given Glassdoor URL and saves the data to a JSON file."

    def _run(self, url: str) -> str:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.RequestException as e:
            return f"Failed to fetch content from {url}: {str(e)}"
        
        database_url = "http://localhost:8000/job"

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = soup.find_all("li", class_="JobsList_jobListItem__wjTHv")

            jobs_data = []

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

                # jobs_data.append(job_data)
                # Data.post(database_url, json=job_data)
                requests.post(database_url, json=job_data)

            # # Post the job data to the database
            # print(jobs_data)
            # for json_data in jobs_data:
            #     try:
            #         Data.post(database_url, json=json_data)
            #     except Exception as e:
            #         return f"Failed to post data to database: {str(e)}"

            return f"Data successfully scraped and posted."

        else:
            return f"Failed to fetch content from {url}. HTTP Status Code: {response.status_code}"



