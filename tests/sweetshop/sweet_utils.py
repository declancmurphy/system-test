#
# Common utilities, definitions and fixtures for SweetShop test suite
#

import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import tests.common as common

##### Variables #####
# Directories
SWEETS_DIR = os.path.join(common.TESTS_DIR, "sweetshop")
SWEETS_DATA_DIR = os.path.join(SWEETS_DIR,"test_data")
SWEETS_PAGES_DIR = os.path.join(SWEETS_DIR,"pages")

# Valid user details
VALID_USER_EMAIL = "test@user.com"
VALID_USER_PWD = "qwerty"



##### Fixtures #####
@pytest.fixture(scope="function")
def driver():
    """
    Used to spawn up selenium webdriver (currently fixed using chrome).
    Can be supplied a headless arg (see .env and docker-compose.yml).
    Yields driver for use in tests and tears down after executing test finishes.
    """
    # Instantiate options object
    options = Options()

    # Driver options
    # # Enable headless mode if HEADLESS=1 (default)
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()

    # Yield driver instance to function using fixture
    yield driver

    # Teardown - quit webdriver session
    driver.quit()