from playwright.sync_api import Page

from pages.create_users_page import CreateUsersPage
from pages.list_all_users_page import ListAllUsersPage
from pages.user_dialogs_page import UserDialogsPage
from pages.user_overlap_page import UserSearchOverlapPage
from utils.playwright_utils import PlaywrightUtils

class DashboardPage():
    """Page object for the Dashboard page.
    """
    
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        
    CREATE_USER_LINK = "//a[@href='/create-user']"
    LIST_ALL_USERS_LINK = "//a[@href='/users']"
    USER_DIALOGS_LINK = "//a[@href='/user-dialogs']"
    USER_SEARCH_OVERLAP_LINK = "//a[@href='/user-search-overlap']"      
    LOADING_SPINNER = ".spinner"  

    def open_create_users_page(self):
        """
        Navigate to the Create Users
        
        Returns:
            CreateUsersPage: An instance of the CreateUsersPage class.
        """
        self.logger.info("Clicking Create Users link")
        self.page.locator(self.CREATE_USER_LINK).click()
        
        return CreateUsersPage(self.page, self.logger)
    
    def open_list_all_users_page(self) -> ListAllUsersPage:
        """
        Open the List All Users page.
        
        Returns:
            ListAllUsersPage: Page object for the List All Users page.
        """
        self.logger.info("Clicking list all users link")
        self.page.click(self.LIST_ALL_USERS_LINK)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return ListAllUsersPage(self.page, self.logger)
    
    def open_user_dialogs_page(self) -> 'UserDialogsPage':
        """
        Open the User Dialogs page.
        
        Returns:
            UserDialogsPage: Page object for the User Dialogs page.
        """
        self.logger.info("Clicking user dialogs link")
        self.page.click(self.USER_DIALOGS_LINK)
        
        return UserDialogsPage(self.page, self.logger)
    
    def open_user_search_overlap_page(self) -> 'UserSearchOverlapPage':
        """
        Open the User Search Overlap page.
        
        Returns:
            UserSearchOverlapPage: Page object for the User Search Overlap page.
        """
        self.logger.info("Clicking user search overlap link")
        self.page.click(self.USER_SEARCH_OVERLAP_LINK)
        
        return UserSearchOverlapPage(self.page, self.logger)    