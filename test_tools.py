
import time
import requests
from bs4 import BeautifulSoup
import json

from src.utils.data import Data

# URL to scrape
url = "https://www.glassdoor.com/Job/germany-software-developer-jobs-SRCH_IL.0,7_IN96_KO8,26.htm"
database_url = "http://localhost:8000/job"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = soup.find_all("li", class_="JobsList_jobListItem__wjTHv")
    print(f"Found {len(job_listings)} job listings")

    # print(job_listings)

    jobs_data = []

    num = 1
    for job in job_listings:
        print(num)
        num+=1
        title = job.find("a", class_="JobCard_jobTitle___7I6y")
        title = title.text.strip() if title else "Not provided"
        
        company = job.find("span", class_="EmployerProfile_compactEmployerName__LE242")
        company = company.text.strip() if company else "Not provided"
        
        location = job.find("div", class_="JobCard_location__rCz3x")
        location = location.text.strip() if location else "Not provided"
        
        description_div = job.find("div", class_="JobCard_jobDescriptionSnippet__yWW8q")
        description = description_div.text.strip() if description_div else "Not provided"
        

        skills = ""
        if "Skills:" in description:
            parts = description.split("Skills:")
            description = parts[0].strip()
            skills = parts[1].strip()
        
        url = job.find("a", class_="JobCard_trackingLink__GrRYn")
        url = url['href'] if url else "Not provided"
        full_url = f"https://www.glassdoor.com{url}" if url != "Not provided" else "Not provided"

        job_data = {
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "skills": skills,
            "url": full_url
        }

        # print(job_data)
        job_json = json.dumps(job_data)
        jobs_data.append(job_json)

        # print(jobs_data)

    for job in jobs_data:
        print(job)
        resp = requests.post(url=database_url, json=job)
        print(resp.status_code)
        time.sleep(1)

    # print(jobs_data[0])

    # for json_data in jobs_data:
    #     requests.post(database_url, json=json_data)
        # time.sleep(1) 

    # with open("glassdoor_jobs.json", "w", encoding="utf-8") as jsonfile:
    #     json.dump(jobs_data, jsonfile, indent=4, ensure_ascii=False)

    print("Data saved to glassdoor_jobs.json")

else:
    print(f"Failed to fetch content from {url}")