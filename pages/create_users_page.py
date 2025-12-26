from utils.playwright_utils import PlaywrightUtils


class CreateUsersPage():
    """
    Page object for the Create Users page.
    """
    
    def __init__(self, page, logger):
        self.page_path = "/create-user"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()

    CREATE_10_USERS_BUTTON = '//button[text()="Create 10 Users"]'  
    
    def wait_for_page_load(self, timeout=5000):
        """
        Wait for the Create Users page to load by checking for the presence of the URI.
        Args:
            timeout (int): Maximum time to wait for the page to load in milliseconds.
        """
        self.logger.info("Waiting for Create Users page to load")
        self.page.wait_for_url(f"**{self.page_path}", timeout=timeout)
        
    def is_at(self):
        """
        Verify that we are on the Create Users page by checking for the presence of a mandatory element.
        Returns:
            bool: True if on the Create Users page, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.CREATE_10_USERS_BUTTON)