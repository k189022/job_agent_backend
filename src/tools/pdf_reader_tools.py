from crewai_tools import BaseTool

class PDFReaderSummarizer(BaseTool):
    name: str = "PDF Reader and Summarizer"
    description: str = "Reads summarizes the content to suggest job types based on skills and education."

    def _run(self,) -> str:
        extracted_text = "Extracted and summarized text from the Lebenslauf, find the background education, softskills and work experience"  # placeholder
        job_suggestions = f"List of suggested job types based on the {extracted_text}"
        return job_suggestions
