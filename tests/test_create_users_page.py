"""
Test suite for the create users page.
"""
import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL

# create venv: python -m venv .venv
# activate venv: .\.venv\Scripts\activate
# install dependencies: pip install -r requirements.txt
# install browsers (will be installed locally): playwright install
# run tests in Chrome: pytest -m smoke --browser chromium --headed -v --html=reports/report.html --self-contained-html
# run tests in Docker: pytest -m smoke --browser chromium -v --html=reports/report.html --self-contained-html
@pytest.mark.smoke
def test_access_create_users_page(page: Page, logger, screenshot):
    """
    Test access to the create users page
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    create_users_page = dashboard_page.open_create_users_page()
    
    assert create_users_page.is_at(), "Failed to access create users page"
