import pytest
import json

import tests.airportgap.api_utils as utils
from tests.airportgap.api_utils import load_iata_data
from tests.airportgap.api_utils import load_distance_data
from tests.airportgap.api_utils import send_request


#################### Tests ####################
def test_get_airports():
    """Verifies successful GET request to the /airports/ endpoint."""
    # Send a request using get_airports key
    response = send_request(utils.AIRPORTS_URL, "GET")

    # Basic assertation to get data is returned
    assert "data" in response.json()
    assert response.status_code == 200

@pytest.mark.parametrize("airport_data", load_iata_data())
def test_get_airport_by_id(airport_data):
    """
    Verifies that GET requests to the "/airports/:id" endpoint return the
    expected response.
    Uses parameterised test data from "iata.json" to test valid/invalid IDs.
    """

    # from loaded test data
    id = airport_data["id"]

    # Send a request using modifed get_airports key url
    url = f"{utils.AIRPORTS_URL}/{id}"
    response = send_request(url, "GET")

    # check response type based on IATA validity
    if airport_data["valid"] == "yes":
        assert response.status_code == 200
        assert "data" in response.json()
    else:
        assert response.status_code == 404

@pytest.mark.parametrize("distance_data", load_distance_data())
def test_post_aiports_distance(distance_data):
    """
    Basic test to verify distance calculation between two airports by IATA codes
    by sending a POST request to the "/airports/distance" endpoint.
    """

    # test data
    test_data = {
        "from": distance_data["from"],
        "to": distance_data["to"]
    }
    expected_distance = distance_data["distance"]
    
    # send request
    response = send_request(utils.DISTANCE_URL, "POST", json=test_data)
    json_response = response.json()
    
    # check good response and that distance is as expected
    assert response.status_code == 200
    assert "data" in json_response
    assert json_response["data"]["attributes"]["kilometers"] == expected_distance