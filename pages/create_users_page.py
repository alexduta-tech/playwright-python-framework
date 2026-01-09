from playwright.sync_api import Page
from utils.config import IMPLICIT_WAIT
from utils.playwright_utils import PlaywrightUtils
from utils.constants import MESSAGE_CREATE_10_USERS_SUCCESS_TEXT, MESSAGE_CREATE_USER_ERROR_REQUIRED_FIELDS_TEXT, MESSAGE_CREATE_USER_SUCCESS_TEXT

class CreateUsersPage():
    """
    Page object for the Create Users page.
    """
    
    def __init__(self, page: Page, logger):
        self.page_path = "/create-user"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.wait_for_page_load()

    # Locators
    BUTTON_BACK_TO_DASHBOARD = "//button[contains(.,'Back')]"
    BUTTON_CREATE_USER = "//button[text()='Create User']"
    BUTTON_CREATE_10_USERS = "//button[text()='Create 10 Users']"
    MESSAGE_GENERIC_LOCATOR = lambda self, msg: f"//div[text()='{msg}']"
    INPUT_NAME = "#name"
    INPUT_EMAIL = "#email"
    INPUT_PROFILE_PHOTO = "//input[@type='file']"
    SELECT_ROLE = "#role"
    SELECT_STATUS = "#status"
    LOADING_SPINNER = "#spinner"  
    
        
    # Page Object Methods
    def wait_for_page_load(self, timeout=IMPLICIT_WAIT):
        """
        Wait for the Create Users page to load by checking for the presence of the URI.
        Args:
            timeout (int): Maximum time to wait for the page to load in milliseconds.
        """
        self.logger.info("Waiting for Create Users page to load")
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
    
    def click_create_user_button(self) -> 'CreateUsersPage':
        """
        Click the Create User button.
        """
        self.logger.info("Clicking Create User button")
        self.page.click(self.BUTTON_CREATE_USER)
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")
        
        return self
    
    def create_10_users(self) -> 'CreateUsersPage':
        """
        Click the Create 10 Users button.
        """
        self.logger.info("Clicking Create 10 Users button")
        self.page.click(self.BUTTON_CREATE_10_USERS)
        # wait for possible loading spinner to disappear
        self.page.wait_for_selector(self.LOADING_SPINNER, state="detached")
        
        return self    
    
    def is_required_fields_error_displayed(self) -> bool:
        """
        Check if the required fields error message is displayed.
        
        Returns:
            bool: True if the error message is displayed, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.MESSAGE_GENERIC_LOCATOR(MESSAGE_CREATE_USER_ERROR_REQUIRED_FIELDS_TEXT))    
    
    def fill_user_form(self, name, email, role, status, profile_photo_path=None) -> 'CreateUsersPage':
        """
        Fill the user creation form with provided details.
        
        Args:
            name: User's name
            email: User's email
            role: User's role
            status: User's status
            profile_photo_path: Path to the profile photo file (optional)
        """
        self.logger.info("Filling user creation form")
        self.logger.info(f"Name: {name}")
        self.page.fill(self.INPUT_NAME, name)
        self.logger.info(f"Email: {email}")
        self.page.fill(self.INPUT_EMAIL, email)
        
        # Select role and status
        self.logger.info(f"Role: {role}")
        self.page.select_option(self.SELECT_ROLE, role)
        self.logger.info(f"Status: {status}")
        self.page.select_option(self.SELECT_STATUS, status)
        
        if profile_photo_path:
            self.logger.info(f"Uploading profile photo from: {profile_photo_path}")
            self.page.set_input_files(self.INPUT_PROFILE_PHOTO, profile_photo_path)
            
        return self

    def is_user_created(self) -> bool:
        """
        Check if the user creation success message is displayed.
        
        Returns:
            bool: True if the success message is displayed, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.MESSAGE_GENERIC_LOCATOR(MESSAGE_CREATE_USER_SUCCESS_TEXT))        
            
    def are_10_users_created(self) -> bool:
        """
        Check if the user creation success message for 10 users is displayed.
        
        Returns:
            bool: True if the success message is displayed, False otherwise.
        """
        return self.playwright_utils.is_element_present(self.MESSAGE_GENERIC_LOCATOR(MESSAGE_CREATE_10_USERS_SUCCESS_TEXT))