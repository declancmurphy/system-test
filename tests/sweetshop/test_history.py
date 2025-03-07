import pytest
import json
from selenium.webdriver.common.by import By

import tests.sweetshop.sweet_utils as utils
from tests.sweetshop.sweet_utils import driver
from tests.sweetshop.pages.login_page import LoginPage
from tests.sweetshop.pages.basket_page import BasketPage
from tests.sweetshop.pages.product_page import ProductPage

#################### Tests ####################
def test_order_history_view(driver):
    """Tests basic display of order history."""
    # Page instantiation using driver fixture
    login_page = LoginPage(driver)

    # Navigate to login page
    login_page.navigate_to(driver)

    # Attempt login using valid credentials
    # note: using field placeholder values and not using login_page.login 
    #       as it fails with current assertions
    login_page.enter_text(login_page.USERNAME_FIELD, utils.VALID_USER_EMAIL)
    login_page.enter_text(login_page.PASSWORD_FIELD, utils.VALID_USER_PWD)
    login_button = driver.find_element(By.XPATH, login_page.LOGIN_BUTTON)
    login_button.click()

    # Check order history is displayed
    assert "Previous Orders" in driver.page_source
    assert "Item Order Breakdown" in driver.page_source

    order_table = driver.find_element(By.XPATH, "//table[@id='transactions']")
    assert order_table.is_displayed()

    order_chart = driver.find_element(By.XPATH, "//canvas[@id='transactionChart']")
    assert order_chart.is_displayed()

# def test_history_updated(driver):
    # """
    # Add test to check order history is updated once user login
    # functionality and order tracking / database is fixed
    # """