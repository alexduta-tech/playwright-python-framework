"""
Test suite for the overlapping scenario page
"""
import pytest

from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL

@pytest.mark.parametrize("expected_message", [
    "Random user:"
],ids=["Overlapping elements completed successfully"])
@pytest.mark.smoke
def test_overlaping_elements(page, logger, expected_message):
    """
    Test Overlapping Scenario
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    overlapping_elements_page = dashboard_page.open_user_search_overlap_page()        
    overlapping_elements_page.click_get_random_user_button()
    
    actual_message = overlapping_elements_page.get_result_message()
    assert expected_message in actual_message, f"Expected message '{expected_message}' not found in actual message '{actual_message}'"