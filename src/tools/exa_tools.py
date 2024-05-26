import os
from dotenv import load_dotenv
from exa_py import Exa
from langchain.agents import tool

class ExaSearchToolset():
    
    @tool
    def search(query: str):
        """Search for a webpage based on the query"""

        result = ExaSearchToolset._exa().search(f"{query}", use_autoprompt=True, num_results=5)
        return result
    
    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """

        result = ExaSearchToolset._exa().find_similar(url, num_results=5)
        return result
    
    @tool
    def get_contents(ids: str):
        """Get the contents of the webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """

        ids = eval(ids)
        contents = str(ExaSearchToolset._exa().get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)
    
    @staticmethod
    def tools_job_search():
        return[
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar
            # ExaSearchToolset.get_contents
        ]
    
    @staticmethod
    def tools_get_details():
        return[
            ExaSearchToolset.search,
            ExaSearchToolset.get_contents
        ]

    def _exa():
        load_dotenv()  # Ensure environment variables are loaded
        api_key = os.getenv('EXA_API_KEY')
        if not api_key:
            raise EnvironmentError("EXA_API_KEY is not set in the environment variables.")
        return Exa(api_key=api_key)
