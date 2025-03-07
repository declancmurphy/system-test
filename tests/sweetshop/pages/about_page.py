#
# Not currently used, but example of future-proofing framework by adding page/page classes to POM
#

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.sweetshop.pages.base_page import BasePage

class AboutPage(BasePage):
    def __init__(self, driver):
        """Initialise with about page URL based on inherited base_url."""
        super().__init__(driver)

        self.url = f"{self.base_url}/about"

    def navigate_to(self, driver):
        """Navigate to about page"""
        driver.get(self.url)