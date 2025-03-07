from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        """Initialise with base URL based on inherited base_url."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = "https://sweetshop.netlify.app"

    def enter_text(self, locator, text):
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text