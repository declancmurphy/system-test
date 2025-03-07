import pytest
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tests.sweetshop.sweet_utils as utils
from tests.sweetshop.sweet_utils import driver
from tests.sweetshop.pages.base_page import BasePage
from tests.sweetshop.pages.login_page import LoginPage
from tests.sweetshop.pages.basket_page import BasketPage
from tests.sweetshop.pages.product_page import ProductPage


###### Functions #####
def load_product_data():
    """Load products for parameterising tests."""

    with open(f"{utils.SWEETS_DATA_DIR}/products.json") as f:
        return json.load(f)


##### Fixtures #####
@pytest.fixture(scope="function")
def setup_basket(driver):
    """
    Setup fixture for basket operations tests, adds a product to basket
    and returns the instantiated POM classes for product/basket pages.
    """

    # Test data for product
    product = "Chocolate Cups"

    # Instantiate required pages
    product_page = ProductPage(driver)
    basket_page = BasketPage(driver)

    # Ensure basket is empty
    basket_page.navigate_to(driver)
    basket_page.empty_basket(driver)

    # Add a product to the basket
    product_page.navigate_to(driver)
    product_page.add_product_to_basket(driver, product, 1)

    # Navigate to basket page for test
    basket_page.navigate_to(driver)

    # Return page class instantiations and product name for use in tests
    yield driver, product_page, basket_page, product

    # Teardown: empty items from basket
    basket_page.navigate_to(driver)
    basket_page.empty_basket(driver)


#################### Tests ####################

@pytest.mark.parametrize("product_data", load_product_data())
def test_add_product_to_basket(driver, product_data):
    """
    Attempt to add each product to basket the specified number of times
    called function should check products exist and that the products
    are added to basket via navbar.
    """

    # instantiate pages
    product_page = ProductPage(driver)
    basket_page = BasketPage(driver)

    # Ensure basket is empty
    basket_page.navigate_to(driver)
    basket_page.empty_basket(driver)

    # Navigate to product page
    product_page.navigate_to(driver)

    # add parameterised items to basket
    product_page.add_product_to_basket(driver, product_data["product_name"], product_data["quantity"])

    # Navigate to basket page
    product_page.navigate_to(driver)

    # check basket has increased to quantity
    assert basket_page.get_basket_quantity(driver) == int(product_data["quantity"])

def test_delete_product_via_basket_page(setup_basket):
    """
    Adds a product to basket and attempts to delete it.
    """

    # unpack returned items from setup fixture
    driver, product_page, basket_page, product = setup_basket

    # attempt to delete product
    basket_page.delete_product(driver, product)

    # check product no longer in basket
    assert basket_page.get_basket_quantity(driver) == 0

def test_empty_basket(setup_basket):
    """Verifies the Empty Basket functionality."""

    # unpack returned items from setup fixture
    driver, product_page, basket_page, product = setup_basket

    # verify basket is not empty
    assert basket_page.get_basket_quantity(driver) > 0

    # attempt to empty basket
    basket_page.empty_basket(driver)

    # assert basket empty
    assert basket_page.get_basket_quantity(driver) == 0

def test_valid_checkout_form_data(setup_basket):
    """
    Attempts to add a product to basket and submit the checkout
    form with parameterised/loaded checkout form data.
    """

    # unpack returned items from setup fixture
    driver, product_page, basket_page, product = setup_basket

    # valid test data for checkout form
    checkout_data = {
        "first_name": "Test",
        "last_name": "Valid",
        "email": "test@valid.com",
        "address_1": "1 Valid Road",
        "zip": "TE57 1NG",
        "card_name": "Valid Card Name",
        "card_number": "1234567812345678",
        "expiry": "123",
        "cvv": "321"
    }

    # Fill out the form using loaded test data
    basket_page.fill_checkout_form(driver, checkout_data)

    # Submit form
    basket_page.submit_form(driver)

    # Check successful form submission (will fail as functionality broken)
    assert "Order Confirmation" in driver.page_source
    assert basket_page.current_url != basket_page.url
   
def test_invalid_checkout_form_data_email(setup_basket):
    """
    Verifies that using an email addressing without an '@' symbol
    displays an error message.
    """

    # unpack returned items from setup fixture
    driver, product_page, basket_page, product = setup_basket

    # invalid test data for checkout form
    checkout_data = {
        "first_name": "Test",
        "last_name": "InvalidEmail",
        "email": "testinvalid.com",
        "address_1": "1 Valid Road",
        "zip": "TE57 1NG",
        "card_name": "Valid Card Name",
        "card_number": "1234567812345678",
        "expiry": "123",
        "cvv": "321"
    }

    # Fill out the form using loaded test data
    basket_page.fill_checkout_form(driver, checkout_data)

    # Submit form
    basket_page.submit_form(driver)


    error = driver.find_element(By.XPATH, "//div[@class='invalid-feedback' and preceding-sibling::input[@id='email']]")
    assert error.is_displayed()