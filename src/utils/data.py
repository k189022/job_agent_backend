import httpx
import asyncio

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
    async def post(url, json, user_id):
        print("post success")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=json, user_id=user_id)
                print(response.status_code)
                if response.status_code == 201:
                    print("Job details saved to database successfully!")
                else:
                    print(f"Failed to save job details. Status code: {response.status_code}")
                    print(json)
            except httpx.RequestError as e:
                print(f"An error occurred: {str(e)}")
                print(json)
