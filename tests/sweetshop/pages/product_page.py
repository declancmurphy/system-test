import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from tests.sweetshop.pages.base_page import BasePage

class ProductPage(BasePage):
    # Define common product-related xpaths
    # BASKET_ITEMS = '//a[contains(@href, "basket")]//span'
    BASKET_ITEMS = '//a[@href="/basket"]//span[@class="badge badge-success"]'
    # BASKET_ITEMS = 'badge badge-success'
    

    def __init__(self, driver):
        """Initialise browse products page"""
        super().__init__(driver)

        # define products page URL
        self.url = f"{self.base_url}/sweets"

    def navigate_to(self, driver):
        """Navigate to the browse products page"""
        driver.get(self.url)

    def add_product_to_basket(self, driver, product_name: str, quantity: int):
        """
        Attempts to add {product_name} to the basket {quantity} times.
        """
        # Define xpath for product "Add to Basket" button based on product name
        product_xpath = f"//a[@data-name='{product_name}']"
        product_button = driver.find_element(By.XPATH, product_xpath)

        # add product to basket specified quantity times
        for i in range(quantity):

            # Add specified product to basket (handle errors, e.g. product not found)
            try:
                product_button.click()
            except NoSuchElementException:
                # Add to Basket button not found for passed product_name
                pytest.fail(f"Product '{product_name}' not found on page.")
            except Exception as e:
                # general exception handling (e.g. button not clickable)
                pytest.fail(f"Error attempting to add {product_name} to basket: {e}")
