class PlaywrightUtils:
    """Utility class for Playwright-related helper methods.
    """
    
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
    
    def is_element_present(self, selector: str) -> bool:
        """
        Check if an element is present on the page.
        Args:
            selector (str): CSS selector, XPath, or Playwright text selector.
        Returns:
            bool: True if element is present, False otherwise.
        """
        elements = self.page.locator(selector)
        count = elements.count()
        return count > 0