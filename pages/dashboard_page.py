from pages.create_users_page import CreateUsersPage


class DashboardPage():
    """Page object for the Dashboard page.
    """
    
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        
    CREATE_USER_LINK = "//a[@href='/create-user']"
    
    def open_create_users_page(self):
        """
        Navigate to the Create Users
        
        Returns:
            CreateUsersPage: An instance of the CreateUsersPage class.
        """
        self.logger.info("Clicking Create Users link")
        self.page.locator(self.CREATE_USER_LINK).click()
        
        return CreateUsersPage(self.page, self.logger)