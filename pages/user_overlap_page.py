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
        
   # Locators  
    BUTTON_BACK_TO_DASHBOARD = "//button[contains(.,'Back')]"
    BUTTON_GET_RANDOM_USER = "#getRandomUserBtn"  
    MESSAGE_SUCCESS = ".message.success"
    MESSAGE_ERROR = ".message.error"
    LOADING_SPINNER = ".spinner"
    
    # Page Object Methods
    def wait_for_page_load(self, timeout=5) -> None:
        """
        Wait for the User Search Overlap page to load by checking the presence of the uri.
        
        Args:
            timeout: Maximum time to wait in seconds
        """
        self.logger.info("Waiting for User Search Overlap page to load")
        self.page.wait_for_url(f"**{self.page_path}", timeout=timeout)     
        
    def go_back_to_dashboard(self) -> None:
        """
        Go back to the Dashboard page.
        """
        self.logger.info("Clicking back to dashboard button")
        self.page.click(self.BUTTON_BACK_TO_DASHBOARD)  
        
    def is_at(self) -> bool:
        """
        Verify that we are on the User Search Overlap page by checking for the presence of a mandatory element.
        
        Returns:
            bool: True if on User Search    Overlap page, False otherwise
        """
        return self.playwright_utils.is_element_present(self.BUTTON_GET_RANDOM_USER)      
    
    def click_get_random_user_button(self) -> 'UserSearchOverlapPage':
        """
        Click the Get Random User button.
        """
        self.logger.info("Clicking get random user button")
        # The button is overlapped by another element, with Playwright we do not need o scroll as this is automatically done
        self.page.click(self.BUTTON_GET_RANDOM_USER)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self

    def get_result_message(self) -> str:
        """
        Get the text of the result message (after interacting with the overlapped element).

        Returns:
            str: The text of the success message or error message if present
        """
              
        # error message is present but was not expected
        if self.playwright_utils.is_element_present(self.MESSAGE_ERROR):
            self.logger.error("Error message present on the page, no success message available")
            return self.page.text_content(self.MESSAGE_ERROR)

        # success message is not present but it was expected
        if not self.playwright_utils.is_element_present(self.MESSAGE_SUCCESS):
            self.logger.error("Success message not present on the page")
            return "Success message not present on the page"
        
        # success message is present
        success_message = self.page.text_content(self.MESSAGE_SUCCESS)
        self.logger.info(f"Success message is present on the page, text: {success_message}")
        
        return success_message               