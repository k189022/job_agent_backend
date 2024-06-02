import httpx
import asyncio

from src.monggoDB.models.job import JobModel
from src.routers.job import create_job

class Data:
    @staticmethod
    async def get(url):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    jobs_list = response.json()  # This parses the JSON data into a Python list/dictionary
                    print("Load data success")
                    return jobs_list
                else:
                    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            except httpx.RequestError as e:
                print(f"An error occurred: {str(e)}")

    @staticmethod
    async def post(json, user_id):
        try:
            await create_job(user_id, json)
            print("Job details saved to database successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")