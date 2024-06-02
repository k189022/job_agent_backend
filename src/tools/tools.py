from crewai_tools import SerperDevTool, ScrapeWebsiteTool, SeleniumScrapingTool
from .glassdoor_scrapper import GlassdoorScraperTool


class Tools():
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    selenium_tool = SeleniumScrapingTool(css_element="JobsList_jobListItem__wjTHv")
    glassdoor_tool = GlassdoorScraperTool()