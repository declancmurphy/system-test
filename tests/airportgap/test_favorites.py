import pytest
import requests
import json

import tests.airportgap.api_utils as utils
from tests.airportgap.api_utils import favorites_setup
from tests.airportgap.api_utils import load_user_data
from tests.airportgap.api_utils import send_request


#################### Tests ####################
# parameterise all tests to responses for valid/invalid tokens
mark as last test in suite using pytest-order so rate limit doesn't inhibit function of other tests
@pytest.mark.parametrize("user_data", load_user_data())
def test_get_favorites(favorites_setup, user_data):
    """
    Verifies GET requests to /favorites/ endpoint
    """
   
    # construct auth header using test data
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}
    
    # send request
    response = send_request(utils.FAVORITES_URL, "GET", headers=headers)
    json_response = response.json()
    
    # check authenticated response
    if user_data["auth"] == "yes":
        assert response.status_code == 200
        response_data = json_response["data"]
        # check correct favorite returned
        assert favorites_setup in response_data
    else:
        # bad auth
        assert response.status_code == 401
    
@pytest.mark.parametrize("user_data", load_user_data())
def test_get_favorites_by_id(favorites_setup, user_data):
    """
    Verifies GET requests to /favorites/:id endpoint
    """
    # from setup fixture
    favorite_id = favorites_setup["id"]
    
    # construct auth header using test data
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}
    
    # send GET request
    response = requests.get(f"{utils.FAVORITES_URL}/{favorite_id}", "GET", headers=headers)
    json_response = response.json()
    
    # check authenticated response
    if user_data["auth"] == "yes":
        assert response.status_code == 200
        
        # check correct favorite returned
        response_data = json_response["data"]
        assert favorites_setup == response_data
    else:
        assert response.status_code == 401


    
@pytest.mark.parametrize("user_data", load_user_data())
def test_post_favorites(user_data):
    """
        Verifies POST request to /favorites endpoint
    """
        
    # construct test data 
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}
    favorite = {"airport_id": "JFK"}
    
    # first ensure no favorites against valid user
    send_request(utils.FAVORITES_CLEAR_URL, "DELETE", headers=headers)

    # send POST request
    response = send_request(utils.FAVORITES_URL, "POST", json=favorite, headers=headers)
    json_response = response.json()
    
    # check response
    if user_data["auth"] == "yes":
        assert response.status_code == 201
        
        response_data = json_response["data"]
        assert response_data["attributes"]["airport"]["iata"] == favorite["airport_id"]
        assert response_data["attributes"]["airport"]["name"] == "John F Kennedy International Airport"
    else:
        # bad auth
        assert response.status_code == 401

@pytest.mark.parametrize("user_data", load_user_data())
def patch_favorites_by_id(favorites_setup, user_data):
    """
    Verifies PATCH requests to /favorites/:id endpoint
    """
    
    # from setup fixture
    favorite_id = favorites_setup["id"]
    
    # construct test data
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}
    test_data = {
        "id": {favorite_id},
        "note": "Test note has changed"
    }
    
    # send PATCH request
    response = send_request(f"{utils.FAVORITES_URL}/{favorite_id}", "PATCH", json=test_data, headers=headers)
    json_response = response.json()
    
    # check response
    if user_data["auth"] == "yes":
        assert response.status_code == 201
        
        response_data = json_response["data"]
        # either of the following are good checks
        assert response_data["note"] != favorites_setup["note"]
        assert response_data["note"] == test_data["note"]
    else:
        # bad auth
        assert response.status_code == 401

@pytest.mark.parametrize("user_data", load_user_data())
def delete_favorites_by_id(favorites_setup, user_data):
    """
    Verifies DELETE requests to /favorites/:id endpoint
    """
    # from setup fixture
    favorite_id = favorites_setup["id"]
    
    # construct test data
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}
    
    # send DELETE request
    response = send_request(f"{utils.FAVORITES_URL}/{favorite_id}", "DELETE", headers=headers)

    # check response
    if user_data["auth"] == "yes":
        # authenticated
        assert response.status_code == 204
        
        # verify favorites empty
        response = send_request(utils.FAVORITES_URL, "GET", headers=headers)
        assert response.status_code == 204
    else:
        # bad auth
        assert response.status_code == 401
    
@pytest.mark.parametrize("user_data", load_user_data())
def delete_favorites_clear_all(favorites_setup, user_data):
    """
    Verifies DELETE requests to /favorites/clear_all endpoint
    """
   
    # construct test data
    token = user_data["token"]
    headers = {"Authorization": f"Bearer token={token}"}

    # send DELETE request
    response = send_request({utils.FAVORITES_CLEAR_URL}, "DELETE", headers=headers)

    # check response
    if user_data["auth"] == "yes":
        # authenticated
        assert response.status_code == 204
        
        # verify favorites empty
        response = send_request(utils.FAVORITES_URL, "GET", headers=headers)
        assert response.status_code == 204
    else:
        # bad auth
        assert response.status_code == 401