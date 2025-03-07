from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.sweetshop.pages.base_page import BasePage

import logging
logging.basicConfig(level=logging.INFO)

class LoginPage(BasePage):
    # Common login locators
    USERNAME_FIELD = (By.ID, "exampleInputEmail")
    PASSWORD_FIELD = (By.ID, "exampleInputPassword")
    LOGIN_BUTTON = "//form[contains(@class, 'needs-validation')]//button"
    LOGIN_NAVBAR = (By.XPATH, "//a[@href='/login']")
    YOUR_ACC_MSG = (By.XPATH, "//h1[contains(text(), 'Your Account')]")
    INVALID_EMAIL_MSG = (By.XPATH, "//*[contains(@class, 'invalid-feedback invalid-email')]")

    def __init__(self, driver):
        """Initialise login page."""
        super().__init__(driver)

        # define login page URL
        self.url = f"{self.base_url}/login"
    
    def navigate_to(self, driver):
        """Navigate to login page."""
        driver.get(self.url)

    def login(self, driver, username, password):
        """
            Attempts to log a user in, but checks that a user
            is not already logged in before doing so.
        """

        # Check a user is not already logged in, skips if so
        if self.is_logged_in():
            logging.info("A user is already logged in. Skipping login attempt.")
            return

        # Enter specified user creds into form fields
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)

        # Submit login form
        login_button = driver.find_element(By.XPATH, self.LOGIN_BUTTON)
        login_button.click()

        # verify successful login
        assert self.is_logged_in()
    
    def is_logged_in(self):
        """ 
            For purposes of asserting successful login
            Note: functionality broken, so defining assertation here is hard
            have shown one way to check by use of navbar element
        """

        # Check for "Log In" navbar element
        # Allow time for login to "succeed"
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.LOGIN_NAVBAR)
            )
            # "Log In" found, therefore not logged in
            return False

        except:
            return True