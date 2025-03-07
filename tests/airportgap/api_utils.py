# See https://airportgap.com/docs for API documentation

import os
import requests
import pytest
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import tests.common as common

# Set log level
logging.basicConfig(level=logging.INFO)

##### Variables #####
# Directories
API_DIR = os.path.join(common.TESTS_DIR,"airportgap")
API_DATA_DIR = os.path.join(API_DIR,"test_data")

# Test data
DISTANCE_DATA = os.path.join(API_DATA_DIR, "distances.json")
IATA_DATA = os.path.join(API_DATA_DIR, "iata.json")
USERS_DATA = os.path.join(API_DATA_DIR, "users.json")

# Pre-generated valid API token
# Ideally improve by securing as a envvar or generating on-the-fly
VALID_TOKEN = "9eZuT8qcakNvU2ARsZHVwdYj"

# Endpoints
BASE_URL = "https://airportgap.com/api"
TOKENS_URL = f"{BASE_URL}/tokens"
AIRPORTS_URL = f"{BASE_URL}/airports"
DISTANCE_URL = f"{AIRPORTS_URL}/distance"
FAVORITES_URL = f"{BASE_URL}/favorites"
FAVORITES_CLEAR_URL = f"{FAVORITES_URL}/clear_all"

# HTTP methods available
HTTP_METHODS = ["GET", "POST", "PATCH", "DELETE"]


##### Functions #####
def load_user_data():
    """Loads test user data."""
    
    with open(USERS_DATA) as f:
        return json.load(f)
    
def load_iata_data():
    """Loads test data for airport IATA codes."""
    
    with open(IATA_DATA) as f:
        return json.load(f)
    
def load_distance_data():
    """Loads test data for distances between airports."""
    
    with open(DISTANCE_DATA) as f:
        return json.load(f)

def send_request(url: str, method: str, params=None, json=None, headers=None):
    """
    Attempts to send a request to the specified API endpoint with the specified request type.
    Implements error handling to catch request failures (e.g invalid request type)
    """
    
    # Check valid HTTP method passed in
    if method.upper() not in HTTP_METHODS:
        raise ValueError(f"Unknown HTTP request type specified: {method.upper()}")

    try:
        logging.info(f"Sending {method.upper} request to {url}")

        # attempt to send a request to specified url with specified HTTP method and any extra args
        response = requests.request(method.upper(), url, headers=headers, json=json)
        logging.info(f"Response state code: {response.status_code}")

        return response
    
    except requests.RequestException as e:
        # Generic error handling
        pytest.fail(f"Request failed: {e}")
        

### Fixtures ###
@pytest.fixture(scope="function")
def favorites_setup():
    """
        Setup/teardown fixture for tests that hit "/favorites/:id" endpoint
        with various HTTP methods
        Uses hardcoded valid token for requests made (see "Improvements" in README.md)
        Setup: Adds a favorite IATA code to a user account
        Teardown: Clears all favorites
    """
    # Setup:
    # construct auth header using test data
    headers = {"Authorization": f"Bearer token={VALID_TOKEN}"}
    favorite = {"airport_id": "KIX",
                "note": "Setup note"}
    
    # first ensure no favorites against valid user
    send_request(FAVORITES_CLEAR_URL, "DELETE", headers=headers)
        
    # send a POST request to favorites
    response = send_request(FAVORITES_URL, "POST", json=favorite, headers=headers)
    json_response = response.json()
     
    # retrieve and yield favorite record data for assertations
    data = json_response["data"]
    yield data

    # Teardown
    # hit FAVORITES_CLEAR_URL endpoint to remove favorite
    send_request(FAVORITES_CLEAR_URL, "DELETE", headers=headers)