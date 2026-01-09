from playwright.sync_api import Page
from utils.playwright_utils import PlaywrightUtils

class UserDialogsPage():
    """
    Page object for the Users Dialogs Page.
    """

    def __init__(self, page: Page, logger):
        self.page_path = "/user-dialogs"
        self.page = page
        self.logger = logger
        self.selenium_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()