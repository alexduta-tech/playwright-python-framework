"""
Test suite for the list all users page
"""
from typing import Optional
import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL
from utils.data_generator import random_name, random_email, random_role, random_status, profile_photo, non_existing_name


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
    
@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status)
],ids=["Filter by email"])
@pytest.mark.smoke
def test_filter_users_by_email(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by email
    """
    _create_users(page, logger, name, email, role, status)    
    
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(email=email)
    result = list_all_users_page.is_user_in_list(email=email)
    
    assert result, f"User with email {email} not found in the filtered list"    
 
@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status)
],ids=["Filter by role"])
@pytest.mark.smoke
def test_filter_users_by_role(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by role
    """
    _create_users(page, logger, name, email, role, status)
    
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(role=role)
    result = list_all_users_page.is_user_in_list(role=role)
    
    assert result, f"User with role {role} not found in the filtered list"
    
@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status)
],ids=["Filter by status"])
@pytest.mark.smoke
def test_filter_users_by_status(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by status
    """
    _create_users(page, logger, name, email, role, status)
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(status=status)
    result = list_all_users_page.is_user_in_list(status=status)
    
    assert result, f"User with status {status} not found in the filtered list"
    
@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status)
],ids=["Filter by name, role and status"])    
@pytest.mark.smoke
def test_filter_users_by_name_role_and_status(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by name, role and status
    """
    _create_users(page, logger, name, email, role, status)
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(name=name, role=role, status=status)
    result = list_all_users_page.is_user_in_list(name=name, role=role, status=status)
    
    assert result, f"User with name {name}, role {role}, and status {status} not found in the filtered list"

@pytest.mark.parametrize("name,email,role,status", [
    (non_existing_name, random_email, random_role, random_status) 
],ids=["Filter by non-existing name"])
@pytest.mark.smoke
def test_filter_users_by_non_existing_name(page, logger, screenshot, name, email, role, status):
    """
    Test filtering users by a non-existing name
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(name=name)
    result = list_all_users_page.is_no_users_found_message_displayed()
    
    assert result, "'No users found' message was not displayed for non-existing name filter"

@pytest.mark.smoke
def test_pagination(page, logger, screenshot):
    """
    Test pagination
    """
    logger.info(f"Opening URL: {BASE_URL}")
    page.goto(BASE_URL)
    
    dashboard_page = DashboardPage(page, logger)
    
    # create more than 10 users to enable pagination
    create_users_page = dashboard_page.open_create_users_page()
    create_users_page.create_10_users()
    create_users_page.create_10_users()
    create_users_page.go_back_to_dashboard()
        
    list_all_users_page = dashboard_page.open_list_all_users_page()
    first_page_users = list_all_users_page.get_displayed_users_rows()
    list_all_users_page.go_to_next_page()
    second_page_users = list_all_users_page.get_displayed_users_rows()
    
    assert first_page_users != second_page_users, "Pagination did not change the displayed users"

@pytest.mark.parametrize("name,email,role,status", [
    (random_name, random_email, random_role, random_status) 
],ids=["Reset filters after applying name, role and status filters"])    
@pytest.mark.smoke
def test_reset_filters(page, logger, screenshot, name, email, role, status):
    """
    Test resetting filters
    """
    _create_users(page, logger, name, email, role, status)
    dashboard_page = DashboardPage(page, logger)
    list_all_users_page = dashboard_page.open_list_all_users_page()
    list_all_users_page.filter_users(name=name, role=role, status=status)
    users_before_reset = list_all_users_page.get_displayed_users_rows()
    list_all_users_page.reset_filters()
    users_after_reset = list_all_users_page.get_displayed_users_rows()
    
    assert users_before_reset != users_after_reset, "Filters were not reset"
   
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