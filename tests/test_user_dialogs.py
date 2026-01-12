"""
Test suite for the user dialogs page
"""
import pytest
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL
from utils.data_generator import random_name, random_email, random_role, random_status

@pytest.mark.parametrize("expected_alert_result_message", [
    "Alert result: Alert was shown, random user:",
], ids=["Alert was shown and accepted"])
@pytest.mark.smoke
def test_alert_accept(page, logger, screenshot, expected_alert_result_message):
    """
    Test Alert 
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    create_users_page.go_back_to_dashboard()
    
    # Open Users Dialogs page and interact with alert
    users_dialogs_page = dashboard_page.open_user_dialogs_page()
    users_dialogs_page.click_show_alert_and_accept_it()
    alert_result_message = users_dialogs_page.get_dialog_result_message()

    assert expected_alert_result_message in alert_result_message, f"Expected alert result message to contain '{expected_alert_result_message}', but got '{alert_result_message}'"
    
@pytest.mark.parametrize("expected_confirm_dialog_result_message", [
    "Confirm result: User clicked OK. Random user name:",
], ids=["Confirm dialog was shown and accepted"])
@pytest.mark.smoke
def test_confirm_dialog_accept(page, logger, screenshot, expected_confirm_dialog_result_message):
    """
    Test Confirm Dialog: accept
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    create_users_page.go_back_to_dashboard()    
    
    # Open Users Dialogs page and interact with confirm dialog
    users_dialogs_page = dashboard_page.open_user_dialogs_page()
    users_dialogs_page.click_show_confirm_dialog_and_accept_it()
    confirm_result_message = users_dialogs_page.get_dialog_result_message()

    assert expected_confirm_dialog_result_message in confirm_result_message, f"Expected confirm dialog result message to contain '{expected_confirm_dialog_result_message}', but got '{confirm_result_message}'"
    
    
@pytest.mark.parametrize("expected_confirm_dialog_result_message", [
    "Confirm result: User cancelled the action.",
], ids=["Confirm dialog was shown and cancelled"])
@pytest.mark.smoke
def test_confirm_dialog_cancel(page, logger, screenshot, expected_confirm_dialog_result_message):
    """
    Test Cancel Confirm Dialog: cancel
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    create_users_page.go_back_to_dashboard()    
    
    # Open Users Dialogs page and interact with confirm dialog
    users_dialogs_page = dashboard_page.open_user_dialogs_page()
    users_dialogs_page.click_show_confirm_dialog_and_cancel_it()
    confirm_result_message = users_dialogs_page.get_dialog_result_message(is_error_expected=True)  
    
    assert expected_confirm_dialog_result_message in confirm_result_message, f"Expected confirm dialog result message to contain '{expected_confirm_dialog_result_message}', but got '{confirm_result_message}'"
    
@pytest.mark.parametrize("name,email,role,status,expected_prompt_result_message", [
    (random_name, random_email, random_role, random_status, "User found in the system.")
],ids=["Prompt dialog was shown, text entered and accepted"])
@pytest.mark.smoke
def test_prompt_dialog_enter_text_and_accept(page, logger, screenshot, name, email, role, status, expected_prompt_result_message):
    """
    Test Prompt Dialog: enter text and accept
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.fill_user_form(name, email, role, status)
    create_users_page.click_create_user_button()
    create_users_page.go_back_to_dashboard()    
    
    # Open Users Dialogs page and interact with prompt dialog
    users_dialogs_page = dashboard_page.open_user_dialogs_page()
    users_dialogs_page.click_show_prompt_and_accept_it(name)
    prompt_result_message = users_dialogs_page.get_dialog_result_message()

    assert expected_prompt_result_message in prompt_result_message, f"Expected prompt dialog result message to contain '{expected_prompt_result_message}', but got '{prompt_result_message}'"

@pytest.mark.parametrize("expected_prompt_result_message", [
    "Prompt result: Prompt canceled.",
], ids=["Prompt dialog was shown and cancelled"])   
@pytest.mark.smoke
def test_prompt_dialog_cancel(page, logger, screenshot, expected_prompt_result_message):
    """
    Test Prompt Dialog: cancel
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    users_dialogs_page = dashboard_page.open_user_dialogs_page()    
    users_dialogs_page.click_show_prompt_and_cancel_it()
    prompt_result_message = users_dialogs_page.get_dialog_result_message(is_error_expected=True)    

    assert expected_prompt_result_message in prompt_result_message, f"Expected prompt dialog result message to contain '{expected_prompt_result_message}', but got '{prompt_result_message}'"
    