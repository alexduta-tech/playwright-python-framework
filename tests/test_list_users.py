"""
Test suite for the list all users page
"""
from typing import Optional
import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL
from utils.data_generator import random_name, random_email, random_role, random_status, profile_photo


@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status)
],ids=["Filter by name"])
@pytest.mark.smoke
def test_filter_users_by_name(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by name
    """
    _create_users(page, logger, name=name, email=email, role=role, status=status)
    
    dashboard_page = DashboardPage(page, logger)
    
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(name=name)
    
    result = list_all_users_page.is_user_in_list(name=name)
    
    assert result, f"User with name {name} not found in the filtered list"

# --- HELPER FUNCTIONS ---
def _create_users(page, logger, name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None, status: Optional[str] = None) -> None:
    """
    Create users
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    # create 10 users
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    
    # create a user with provided details
    if name and email and role and status:
        create_users_page.fill_user_form(
            name=name,
            email=email,
            role=role,
            status=status
        )
        create_users_page.click_create_user_button()
        
    create_users_page.go_back_to_dashboard()