from playwright.sync_api import Page

class GenericDialog:
    """
    Page object for the Generic Dialog: alert, confirm, prompt.
    
    In Playwright, native browser dialogs like alert(), confirm(), and prompt() 
    are auto-dismissed by default. 
    This means they will not appear visually during test execution.
    """

    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger
        
    def get_generic_dialog_text(self) -> str:
        """
        Get the text of the dialog.

        Returns:
            str: The text of the alert dialog
        """
        dialog_message = self.page.on("dialog", lambda dialog: dialog.message())
        self.logger.info(f"Dialog text: {dialog_message}")
        return dialog_message
    
    def accept_generic_dialog(self) -> 'GenericDialog':
        """
        Accept the alert/confirm dialog.
        """
        self.logger.info("Accepting generic alert dialog")
        self.page.on("dialog", lambda dialog: dialog.accept())
        
        return self

    def cancel_confirm_or_prompt_dialog(self) -> 'GenericDialog':
        """
        Cancel the confirm/prompt dialog.
        """
        self.logger.info("Cancelling confirm dialog")
        self.page.on("dialog", lambda dialog: dialog.dismiss())
        
        return self

    def send_text_and_accept_prompt_dialog(self, text: str) -> 'GenericDialog':
        """
        Send text to the prompt dialog.

        Args:
            text (str): The text to send to the prompt dialog
        """
        self.logger.info(f"Sending text '{text}' to prompt dialog")
        self.page.on("dialog", lambda dialog: dialog.accept(text))
        
        return self