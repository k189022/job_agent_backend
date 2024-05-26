from crewai_tools import SerperDevTool, ScrapeWebsiteTool, SeleniumScrapingTool
from .glassdoor_scrapper import GlassdoorScraperTool


class Tools():
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    selenium_tool = SeleniumScrapingTool()
    glassdoor_tool = GlassdoorScraperTool()