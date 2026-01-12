from playwright.sync_api import Page

from utils.config import IMPLICIT_WAIT

class PlaywrightUtils:
    """Utility class for Playwright-related helper methods.
    """
    
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger
    
    def is_element_present(self, selector: str, timeout: int = 1000) -> bool:
        """
        Check if an element is present on the page with a timeout.
        Args:
            selector (str): CSS selector, XPath, or Playwright text/role selector.
            timeout (int): Maximum time to wait in milliseconds (default: 1000ms).
        Returns:
            bool: True if element is present, False otherwise.
        """
        self.logger.debug(f"Checking if element is present: {selector}")
        try:
            self.page.locator(selector).wait_for(state="attached", timeout=timeout)
            self.scroll_to_element(selector)
            self.logger.debug(f"Element is present")
            return True
        except Exception:
            self.logger.debug("Element is not present")
            return False
    
    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to the specified element on the page.
        Args:
            selector (str): CSS selector, XPath, or Playwright text selector.
        """
        self.logger.debug(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
        self.logger.debug(f"Scrolled to element")
        
    def wait_for_element_to_disappear(self, selector: str, timeout: int = IMPLICIT_WAIT) -> None:    
        """
        Wait for the element to disappear (if present).
        """
        self.logger.debug(f"Waiting for element to disappear: {selector}")
        self.page.locator(selector).wait_for(state="hidden", timeout=timeout)