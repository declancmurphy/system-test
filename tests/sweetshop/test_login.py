import pytest
import json

import tests.sweetshop.sweet_utils as utils
from tests.sweetshop.sweet_utils import driver
from tests.sweetshop.pages.login_page import LoginPage

### Functions ###
def load_login_data():
    """Load login data for parameterisation."""
    
    with open(f"{utils.SWEETS_DATA_DIR}/login_data.json") as f:
        return json.load(f)

#################### Tests ####################
@pytest.mark.parametrize("login_data", load_login_data())
def test_login(driver, login_data):
    """Verifies login functionality using parameterised data.
    Currently fails due to broken functionality."""
    
    # Page instantiation using driver fixture
    login_page = LoginPage(driver)

    # Navigate to login page
    login_page.navigate_to(driver)

    # Attempt login using parameterised test data
    login_page.login(driver, login_data["email"], login_data["password"])

    if login_data["expected_result"]=="success":
        """
        Verify successful login with valid credentials (supplied via tooltips
        
        Future improvements (once site fixed):
            Use valid credentials in DB
            Test various user permission levels
            assert "account" url suffix rather than current suffix below
            assert "Login" CTA not displayed on header
            assert auth token generated
        """
        # Your Account page header is displayed 
        assert "Your Account" in driver.page_source
        
        # Change the following once login functionality fixed
        assert driver.current_url == f"{login_page.base_url}/00efc23d-b605-4f31-b97b-6bb276de447e.html"

    elif login_data["expected_result"]=="fail" or login_data["expected_result"]=="bad_email":
        """
        Assertations common to all failure modes
        Note: expected to fail due to assumptions made on correct functionality

        Future improvements (once site fixed): 
            assert auth token not generated
        """

        # note: below will currently fail due to bugs mentioned in docs/known_issues.md
        assert driver.current_url == login_page.url

    elif login_data["expected_result"]=="fail":
        """
        Standard failure mode (invaid user credentials)
        Note: currently expected to fail due to assumptions made on correct functionality

        Future improvements:
            change expected error message assertation once implemented
        """

        # note: this failure mode assumes correct login functionality, will currently always fail
        assert "Invalid credentials" in driver.page_source
        
    elif login_data["expected_result"]=="bad_email":
        """
        Invalid email format failure mode

        Note:
            left out the following assertion to prove checking for error message works,
            but should be added when functionality is fixed:
                assert driver.current_url == login_page.url
        """
        error = driver.find_element(login_page.INVALID_EMAIL_MSG)
        assert error.is_displayed()