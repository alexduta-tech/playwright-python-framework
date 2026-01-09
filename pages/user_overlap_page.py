from playwright.sync_api import Page
from utils.playwright_utils import PlaywrightUtils

class UserSearchOverlapPage:
    """
    Page object for the User Search Overlap page (the get random user button is overlapped by another element).
    """
    
    def __init__(self, page: Page, logger):
        self.page_path = "/user-search-overlap"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()