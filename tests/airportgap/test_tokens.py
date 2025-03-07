import pytest
import requests
import json

import tests.airportgap.api_utils as utils
from tests.airportgap.api_utils import load_user_data
from tests.airportgap.api_utils import send_request

#################### Tests ####################
@pytest.mark.parametrize("user_data", load_user_data())
def test_get_token(user_data):
    """
    Basic test to verify tokens endpoint using valid and invalid data
    Uses pre-defined token value to check returned token is correct
    Expected to 
    """
    
    # Define test data (strip auth token)
    data = {
        "email": user_data["email"], 
        "password": user_data["password"]
    }

    # send request
    response = send_request(utils.TOKENS_URL, "POST", json=data)
    json_response = response.json()
    
    # assertation based on expected auth outcome
    if user_data["auth"] == "yes":
        # token found
        assert response.status_code == 200
        assert json_response["token"] == user_data["token"]
    else:
        # unauthorised
        assert response.status_code == 401