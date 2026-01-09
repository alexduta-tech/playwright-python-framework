from playwright.sync_api import Page
from utils.config import IMPLICIT_WAIT
from utils.playwright_utils import PlaywrightUtils

class ListAllUsersPage():
    """Page object for the List All Users page.
    """
    
    def __init__(self, page: Page, logger):
        self.page_path = "/users"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()
        
    # Locators
    BUTTON_BACK_TO_DASHBOARD = "//button[contains(.,'Back')]"
    INPUT_SEARCH = "#searchInput"
    SELECT_ROLE = "#filterRole"
    SELECT_STATUS = "#filterStatus"
    BUTTON_RESET_FILTERS = "//button[text()='Reset Filters']"    
    TABLE_USERS = "table"
    TABLE_USERS_HEADERS = "//table/thead/tr/th"
    TABLE_USERS_ROWS = "//table/tbody/tr"
    TABLE_NO_USERS_FOUND_MESSAGE = "#noUsersCell"
    TABLE_NEXT_PAGE_BUTTON = "#nextPage"
    TABLE_PREVIOUS_PAGE_BUTTON = "#prevPage"
    LOADING_SPINNER = "#spinner"
    
    # Page Object Methods
    def wait_for_page_load(self, timeout=IMPLICIT_WAIT) -> None:
        """
        Wait for the List All Users page to load by checking the presence of the uri.
        
        Args:
            timeout: Maximum time to wait in milliseconds
        """
        self.logger.info("Waiting for List All Users page to load")
        self.page.wait_for_url(f"**{self.page_path}", timeout=timeout)     

    def go_back_to_dashboard(self) -> None:
        """
        Click the Back to Dashboard button.
        """
        self.logger.info("Clicking Back to Dashboard button")
        self.page.click(self.BUTTON_BACK_TO_DASHBOARD)
        
    def is_at(self):
        """
        Verify that we are on the Create Users page by checking for the presence of a mandatory element.
        Returns:
            bool: True if on the Create Users page, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.CREATE_10_USERS_BUTTON) 
    
    def filter_users(self, **kwargs) -> 'ListAllUsersPage':
        """
        Filter users by name, email, role, or status.
        
        Args:
            name: User's name
            email: User's email
            role: User's role
            status: User's status
        
        Args:
            kwargs: Key-value pairs representing user attributes 
                to search for. Examples:
                filter_users(name="John")
                filter_users(email="john@example.com")
                filter_users(name="John", role="Admin", status="Active")
        """
        if kwargs.get('name'):
            self.logger.info(f"Filtering users by name: {kwargs['name']}")
            self.page.fill(self.INPUT_SEARCH, kwargs['name'])
        elif kwargs.get('email'):
            self.logger.info(f"Filtering users by email: {kwargs['email']}")
            self.page.fill(self.INPUT_SEARCH, kwargs['email'])
        if kwargs.get('role'):
            self.logger.info(f"Filtering users by role: {kwargs['role']}")
            self.page.select_option(self.SELECT_ROLE, kwargs['role'])
        if kwargs.get('status'):
            self.logger.info(f"Filtering users by status: {kwargs['status']}")
            self.page.select_option(self.SELECT_STATUS, kwargs['status'])
        
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")
        # wait for the users table to be updated
        self.page.locator(self.TABLE_USERS).wait_for(state="attached", timeout=IMPLICIT_WAIT)        
        return self

    def is_user_in_list(self, **kwargs) -> bool:
        """
        Check if a user with the given attributes is present in the users list.
        
        Args:
            kwargs: Key-value pairs representing user attributes 
                to search for. Examples:
                is_user_in_list(name="John", email="john@example.com")
                is_user_in_list(role="Admin")
        
        Returns:
            bool: True if the user is found, False otherwise.
        """
        is_user_found = True
        self.logger.info(f"Checking if user with attributes {kwargs} is in the list of users")  
        rows = self.page.locator(self.TABLE_USERS_ROWS)
        for row in rows.all():
            # check all provided attributes, ignore case when searching for values
            for key, value in kwargs.items():
                if value.lower() in row.text_content().lower():
                    self.logger.info(f"User attribute '{key}: {value}' was found for row: {row.text_content()}") 
                else:
                    self.logger.error(f"User attribute '{key}: {value}' was not found for row: {row.text_content()}")
                    is_user_found = False
        return is_user_found
    
    def is_no_users_found_message_displayed(self) -> bool:
        """
        Check if the 'No users found' message is displayed.
        
        Returns:
            bool: True if the message is displayed, False otherwise.
        """
        self.logger.info("Checking if 'No users found' message is displayed")
        return self.playwright_utils.is_element_present(self.TABLE_NO_USERS_FOUND_MESSAGE)
    
    def go_to_next_page(self) -> 'ListAllUsersPage':
        """
        Go to the next page of the users list.
        """
        self.logger.info("Clicking next page button")
        self.page.click(self.TABLE_NEXT_PAGE_BUTTON)                             
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")
                
        return self                
    
    def go_to_previous_page(self) -> 'ListAllUsersPage':
        """
        Go to the previous page of the users list.
        """
        self.logger.info("Clicking previous page button")
        self.page.click(self.TABLE_PREVIOUS_PAGE_BUTTON)
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")
        
        return self
    
    def get_displayed_users_rows(self) -> list:
        """
        Get all user rows from the users table.

        Returns:
            list: List of strings representing user row texts.
        """
        self.logger.info("Getting all user rows from the users table")
        result = [row.text for row in self.page.locator(self.TABLE_USERS_ROWS).all()]
        self.logger.debug(f"User rows: {result}")
        
        return result    
    
    def reset_filters(self) -> 'ListAllUsersPage':
        """
        Reset all applied filters.
        """
        self.logger.info("Clicking reset filters button")
        self.page.click(self.BUTTON_RESET_FILTERS)
        
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")        
        
        return self