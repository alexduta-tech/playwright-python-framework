"""
Test suite for the create users page.
"""
import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL
from utils.data_generator import random_name, random_email, random_role, random_status, profile_photo

@pytest.mark.smoke
def test_create_10_users(page: Page, logger, screenshot):
    """
    Test creating 10 users
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    
    assert create_users_page.are_10_users_created(), "10 users were not created successfully"


@pytest.mark.parametrize("name,email,role,status,profile_photo", [
    (random_name, random_email, random_role, random_status, profile_photo)
],ids=["Create user with random data"])
@pytest.mark.smoke
def test_create_user_success(page: Page, logger, screenshot, name, email, role, status, profile_photo):
    """
    Test positive flow for creating a user
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.fill_user_form(
        name=name,
        email=email,
        role=role,
        status=status,
        profile_photo_path=profile_photo
    )
    
    create_users_page.click_create_user_button()
    
    assert create_users_page.is_user_created(), "User was not created"
    
@pytest.mark.smoke
def test_create_user_negative(page: Page, logger, screenshot):
    """
    Test negative flow for creating a user: name and email are required fields
    """    
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    dashboard_page = DashboardPage(page, logger)
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.click_create_user_button()
    
    assert create_users_page.is_required_fields_error_displayed(), "Error message was not displayed for required fields: Name and Email"
