from typing import Optional
from playwright.sync_api import Page
from pages.common_widgets.generic_dialog import GenericDialog
from utils.playwright_utils import PlaywrightUtils

class UserDialogsPage():
    """
    Page object for the Users Dialogs Page.
    """

    def __init__(self, page: Page, logger):
        self.page_path = "/user-dialogs"
        self.page = page
        self.logger = logger
        self.playwright_utils = PlaywrightUtils(self.page, self.logger)
        self.generic_alert_dialog = GenericDialog(self.page, self.logger)
        self.wait_for_page_load()
        
    # Locators
    BUTTON_BACK_TO_DASHBOARD = "//button[contains(.,'Back')]"
    BUTTON_SHOW_ALERT = "#alertBtn"
    BUTTON_SHOW_CONFIRM = "#confirmBtn"
    BUTTON_SHOW_PROMPT = "#promptBtn"
    MESSAGE_SUCCESS = ".message.success"
    MESSAGE_ERROR = ".message.error"
    LOADING_SPINNER = ".spinner"
    
    # Page Object Methods
    def wait_for_page_load(self, timeout=5) -> None:
        """
        Wait for the Users Dialogs page to load by checking the presence of the uri.

        Args:
            timeout: Maximum time to wait in seconds
        """
        self.logger.info("Waiting for Users Dialogs page to load")
        self.page.wait_for_url(f"**{self.page_path}", timeout=timeout)     
        
    def go_back_to_dashboard(self) -> None:
        """
        Go back to the Dashboard page.
        """
        self.logger.info("Clicking back to dashboard button")
        self.page.click(self.BUTTON_BACK_TO_DASHBOARD)  
        
    def is_at(self) -> bool:
        """
        Verify that we are on the Users Dialogs page by checking for the presence of a mandatory element.

        Returns:
            bool: True if on Users Dialogs page, False otherwise
        """
        return self.playwright_utils.is_element_present(self.BUTTON_SHOW_ALERT)                 

    def click_show_alert_and_accept_it(self) -> 'UserDialogsPage':
        """ 
        Click the Show Alert button and accept the alert dialog.
        """           
        # 1. Register the handler BEFORE the action
        self.accept_alert_dialog()
        # 2. Trigger the dialog
        self.logger.info("Clicking Show Alert button")
        self.page.click(self.BUTTON_SHOW_ALERT)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self
    
    def accept_alert_dialog(self) -> 'UserDialogsPage':
        """
        Accept the alert dialog.
        """
        self.logger.info("Accepting alert dialog")
        self.generic_alert_dialog.accept_generic_dialog()
        
        return self        
    
    def get_dialog_result_message(self, is_error_expected=False) -> str:
        """
        Get the text of the dialog result message.

        Returns:
            str: The text of the success message or error message if present
        """
        
        # error message is present and it was expected
        if is_error_expected:
            error_message = self.page.text_content(self.MESSAGE_ERROR)
            self.logger.info(f"Error message is present on the page, text: {error_message}")
            return error_message
        
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
        
    def click_show_confirm_dialog_and_accept_it(self) -> 'UserDialogsPage':
        """ 
        Click the Show Confirm button and accept the confirm dialog. 
        """
        # 1. Register the handler BEFORE the action
        self.accept_confirm_dialog()
        # 2. Trigger the dialog          
        self.logger.info("Clicking show confirm button")
        self.page.click(self.BUTTON_SHOW_CONFIRM)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self
    
    def accept_confirm_dialog(self) -> 'UserDialogsPage':
        """
        Accept the confirm dialog.
        """
        self.generic_alert_dialog.accept_generic_dialog()
        
        return self

    def click_show_confirm_dialog_and_cancel_it(self) -> 'UserDialogsPage':
        """ 
        Click the Show Confirm button and accept the confirm dialog. 
        """
        # 1. Register the handler BEFORE the action
        self.cancel_confirm_dialog()
        # 2. Trigger the dialog          
        self.logger.info("Clicking show confirm button")
        self.page.click(self.BUTTON_SHOW_CONFIRM)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self
        
    def cancel_confirm_dialog(self) -> 'UserDialogsPage':
        """
        Cancel the confirm dialog.
        """
        self.generic_alert_dialog.cancel_confirm_or_prompt_dialog()
        
        return self
    
    def click_show_prompt_and_accept_it(self, text: Optional[str] = None) -> 'UserDialogsPage':
        """ 
        Click the Show Prompt button, send text to the prompt dialog and accept the prompt dialog.
        """           
        # 1. Register the handler BEFORE the action
        self.accept_prompt_dialog_with_text(text)
        # 2. Trigger the dialog
        self.logger.info("Clicking show prompt button")
        self.page.click(self.BUTTON_SHOW_PROMPT)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self

    def accept_prompt_dialog_with_text(self, text: str) -> 'UserDialogsPage':
        """
        Accept the prompt dialog with the provided text.

        Args:
            text (str): The text to send to the prompt dialog
        """
        self.generic_alert_dialog.send_text_and_accept_prompt_dialog(text)
        
        return self

    def click_show_prompt_and_cancel_it(self) -> 'UserDialogsPage':
        """ 
        Click the Show Prompt button and cancel the prompt dialog.
        """           
        # 1. Register the handler BEFORE the action
        self.cancel_prompt_dialog()
        # 2. Trigger the dialog
        self.logger.info("Clicking show prompt button")
        self.page.click(self.BUTTON_SHOW_PROMPT)
        self.playwright_utils.wait_for_element_to_disappear(self.LOADING_SPINNER)
        
        return self
    
    def cancel_prompt_dialog(self) -> 'UserDialogsPage':
        """
        Cancel the prompt dialog.
        """
        self.generic_alert_dialog.cancel_confirm_or_prompt_dialog()
        
        return self
    