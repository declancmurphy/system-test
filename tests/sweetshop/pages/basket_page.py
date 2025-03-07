import logging

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from tests.sweetshop.pages.base_page import BasePage

# Set log level
logging.basicConfig(level=logging.INFO)

class BasketPage(BasePage):
    SUBMIT_BUTTON = "//button[@type='submit']"
    EMPTY_BASKET = "//a[@onclick='emptyBasket();']"
    BASKET_COUNT = "//span[@id='basketCount']"
    
    # form field locators
    FIRST_NAME_INPUT = "//div[label[@for='firstName']]/input[@id='name']"
    LAST_NAME_INPUT = "//div[label[@for='lastName']]/input[@id='name']"
    EMAIL_INPUT = "email"
    ADDRESS_1_INPUT = "address"
    ADDRESS_2_INPUT = "address2"
    ZIP_INPUT = "zip"
    CARD_NAME_INPUT = "cc-name"
    CARD_NUM_INPUT = "cc-number"
    EXPIRY_INPUT = "cc-expiration"
    CVV_INPUT = "cc-cvv"


    def __init__(self, driver):
        """Initialise basket/checkout page"""

        super().__init__(driver)

        # define basket page URL
        self.url = f"{self.base_url}/basket"

    def navigate_to(self, driver):
        """Navigate to basket page"""

        driver.get(self.url)
    
    def delete_product(self, driver, product_name):
        """
        Delete a product from the basket.
        Assumes a product has been added to basket.
        """

        product_xpath = f"//div[.//text()[contains(., '{product_name}')]]//a"
        product_button = driver.find_element(By.XPATH, product_xpath)
        product_button.click()

        # pop-up should now display confirming whether to delete item or not
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()

    def empty_basket(self, driver):
        """Empties the basket. Checks whether already empty before attempting."""

        # only attempt to empty and accept alert if not empty
        if self.get_basket_quantity(driver) != 0:
            empty_basket = driver.find_element(By.XPATH, self.EMPTY_BASKET)
            empty_basket.click()
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()

    def fill_checkout_form(self, driver, checkout_data):
        """Fills the checkout form fields with specified values."""

        # Dropdown select elements (options restricted)
        country_list = Select(driver.find_element(By.ID, "country"))
        city_list = Select(driver.find_element(By.ID, "city"))
    
        # Enter specified payment/delivery into form fields
        self.enter_text((By.XPATH, self.FIRST_NAME_INPUT), checkout_data["first_name"])
        self.enter_text((By.XPATH, self.LAST_NAME_INPUT), checkout_data["last_name"])
        self.enter_text((By.ID, self.EMAIL_INPUT), checkout_data["email"])
        self.enter_text((By.ID, self.ADDRESS_1_INPUT), checkout_data["address_1"])
        country_list.select_by_visible_text("United Kingdom")
        city_list.select_by_visible_text("Bristol")
        self.enter_text((By.ID, self.ZIP_INPUT), checkout_data["zip"])
        self.enter_text((By.ID, self.CARD_NAME_INPUT), checkout_data["card_name"])
        self.enter_text((By.ID, self.CARD_NUM_INPUT), checkout_data["card_number"])
        self.enter_text((By.ID, self.EXPIRY_INPUT), checkout_data["expiry"])
        self.enter_text((By.ID, self.CVV_INPUT), checkout_data["cvv"])

    def submit_form(self, driver):
        """Submit the checkout form."""

        submit_button = driver.find_element(By.XPATH, self.SUBMIT_BUTTON)
        submit_button.click()

    def get_basket_quantity(self, driver):
        """Verifies the basket contains the given quantity of items"""

        driver.get(self.url)
        basket_quantity = driver.find_element(By.XPATH, self.BASKET_COUNT)

        return int(basket_quantity.text)