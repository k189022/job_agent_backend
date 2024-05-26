#!/usr/bin/python3
import requests
import csv
import os
import datetime
import time
import random
from bs4 import BeautifulSoup as soup

url = "https://www.linkedin.com/jobs/search/?currentJobId=3932470490&geoId=101282230&keywords=Machine%20Learning%20Engineer"

def generate_filename(url):
    current_date = datetime.datetime.now().strftime("%m-%d-%Y-%Hh%M")
    filename = f'job_data_{current_date}.csv'
    return filename

def generate_file(csv_filename, job_links):
    headers = ['Source', 'Organization', 'Job Title', 'Location', 'Posted', 'Applicants Hired', 'Seniority Level', 'Employment Type', 'Job Function', 'Industry']
    with open(csv_filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for job_link in job_links:
            job_data = get_job_data(job_link)
            writer.writerow(job_data)

def check_file(filename):
    if filename in os.listdir():
        print(f"\n✅ Successfully generated {filename} file!")

def get_nums(string):
    for word in string.split():
        if word.isdigit():
            return word
    return ""

def change_ip():
    new_ip = f"192.168.1.{random.randint(2, 254)}"
    os.system('sudo ifconfig eth0 down')
    os.system(f'sudo ifconfig eth0 {new_ip}')
    os.system('sudo ifconfig eth0 up')
    print("New IP Address:", new_ip)

def get_job_data(job_link):
    job_data = [job_link]
    for _ in range(5):
        time.sleep(random.randint(1, 3))
        response = requests.get(job_link, headers={'User-agent': 'Mozilla/5.0'})
        if response.status_code == 429:
            print("\n⚠️  Too many requests - Retrying with a new IP...")
            change_ip()
            continue
        response.raise_for_status()
        job_soup = soup(response.text, 'html.parser')
        content = job_soup.find('div', {'class': 'topcard__content-left'})
        if not content:
            continue
        org = content.find('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'}) or \
              content.find('span', {'class': 'topcard__flavor'})
        job_title = content.find('h1', {'class': 'topcard__title'})
        location = content.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'})
        posted = content.find('span', {'class': 'posted-time-ago__text'}) or \
                 content.find('span', {'class': 'posted-time-ago__text--new'})
        applicants = content.find('figcaption', {'class': 'num-applicants__caption'}) or \
                     content.find('span', {'class': 'topcard__flavor--bullet num-applicants__caption'})
        criteria = job_soup.findAll('span', {'class': 'job-criteria__text job-criteria__text--criteria'})[:4]

        job_data.extend([
            org.text if org else '',
            job_title.text.replace(',', '.') if job_title else '',
            location.text.replace(',', '.') if location else '',
            posted.text if posted else '',
            f"{get_nums(applicants.text)} Applicants" if applicants else ''
        ])
        job_data.extend([c.text for c in criteria])
        job_data.extend([''] * (10 - len(job_data)))
        break
    return job_data

def main(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_soup = soup(response.text, 'html.parser')
        
        # Debugging prints to verify HTML structure
        print("Page title:", page_soup.title.string)
        
        # Extract Job Links
        job_links = []
        result_cards = page_soup.findAll("div", {"class": "base-card job-search-card"})
        print(f"Found {len(result_cards)} result cards")

        for res_card in result_cards:
            print("Processing a result card")
            link = res_card.find('a', {'class': 'base-card__full-link'})
            if link:
                print("Found a link:", link['href'])
                job_links.append(link['href'])
            else:
                print("No link found in this result card")

        if not job_links:
            print("\n⚠️  Couldn't extract job links list from LinkedIn, try again later!")
            return

        print(f'\n🕵️  {len(job_links)} recent jobs identified.\n')
        csv_filename = generate_filename(url)
        generate_file(csv_filename, job_links)
        check_file(csv_filename)
        print(f'\n🕵️  Written all information in: {csv_filename}\n')

    except requests.HTTPError as err:
        print(f'❌ Something went wrong!', err)

if __name__ == "__main__":
    main(url)
