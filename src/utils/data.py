import httpx
from src.routers.motivation import create_motivation
from src.routers.template import get_template_for_user
from src.routers.job import create_job

class Data:
    @staticmethod
    async def get(url):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()  # This parses the JSON data into a Python list/dictionary
                    print("Load data success")
                    return data
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


    @staticmethod
    async def get_template(user_id):
        try:
            data = await get_template_for_user(user_id= user_id)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return data

    @staticmethod
    def post_motlet(letter):
        try:
            create_motivation(letter=letter)
            print("motivation letter saved")

        except Exception as e:
            print(f"An error occurred: {str(e)}")