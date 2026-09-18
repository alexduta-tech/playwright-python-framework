from playwright.sync_api import Page

class GenericDialog:
    """
    Page object for the Generic Dialog: alert, confirm, prompt.
    
    In Playwright, native browser dialogs like alert(), confirm(), and prompt() 
    are auto-dismissed by default. 
    This means they will not appear visually during test execution.

    Handlers are registered with page.once so that each one handles exactly the next
    dialog; page.on would keep every handler registered, and a later dialog would be
    handled by all of them.
    """

    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger
        self.last_dialog_message = None
        
    def get_generic_dialog_text(self) -> str:
        """
        Get the text of the most recently handled dialog.

        Playwright reports a dialog through an event that must be answered straight
        away, so the text is recorded by the handler and is available once the dialog
        has been handled, whereas Selenium reads it while the dialog is still open.

        Returns:
            str: The text of the dialog, or None if no dialog has been handled yet
        """
        self.logger.info(f"Dialog text: {self.last_dialog_message}")
        return self.last_dialog_message
    
    def accept_generic_dialog(self) -> 'GenericDialog':
        """
        Accept the alert/confirm dialog.
        """
        self.logger.info("Accepting generic alert dialog")
        self._handle_next_dialog(lambda dialog: dialog.accept())
        
        return self

    def cancel_confirm_or_prompt_dialog(self) -> 'GenericDialog':
        """
        Cancel the confirm/prompt dialog.
        """
        self.logger.info("Cancelling confirm dialog")
        self._handle_next_dialog(lambda dialog: dialog.dismiss())
        
        return self

    def send_text_and_accept_prompt_dialog(self, text: str) -> 'GenericDialog':
        """
        Send text to the prompt dialog.

        Args:
            text (str): The text to send to the prompt dialog
        """
        self.logger.info(f"Sending text '{text}' to prompt dialog")
        self._handle_next_dialog(lambda dialog: dialog.accept(text))
        
        return self

    def _handle_next_dialog(self, respond) -> None:
        """
        Answer the next dialog with `respond`, recording its text first.
        """
        def handler(dialog):
            self.last_dialog_message = dialog.message
            respond(dialog)

        self.page.once("dialog", handler)
