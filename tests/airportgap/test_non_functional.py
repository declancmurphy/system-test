import pytest
import requests
import time

import tests.airportgap.api_utils as utils
from tests.airportgap.api_utils import send_request

RATE_LIMIT = 100

#################### Tests ####################
@pytest.mark.order("last")
def test_rate_limiting():
    """
    Verify that over 100 requests in 1 minute returns a '429 Too Many Requests' 
    response.
    Uses the GET /airports/ endpoint request.
    Marked as last test in suite using pytest-order so rate limit doesn't 
    inhibit function of other tests.
    """

    good_responses = 0
    bad_responses = 0

    # wait 60 seconds as previous tests might affect rate limit point
    time.sleep(60)

    # start timer
    start_time = time.perf_counter()
    
    # Send repeated requests above limit
    for i in range(RATE_LIMIT + 30):
        response = send_request(f"{utils.AIRPORTS_URL}/KIX", "GET")
        
        if response.status_code == 200:
            good_responses += 1
        elif response.status_code == 429:
            # Rate limit response received
            bad_responses += 1
                       
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            # check we hit the rate limit in under 60 seconds (limit resets every minute)
            assert elapsed_time < 60

            # check we hit 100 good responses before rate limit
            assert good_responses == RATE_LIMIT, "Rate limit was not enforced."
            
            break
         
    # ensure we got at least one bad response
    assert bad_responses > 0, f"Rate limit was not enforced. {good_responses} requests made"

def test_response_time():
    """
    Basic performance testing
    Verify that a request response time is received within 1 second.
    Note: could be abstracted out into send_request for comprehensive performance quality assurance
    """

    # make a simple request (GET /airports/:id)
    response = send_request(f"{utils.AIRPORTS_URL}/KIX", "GET")

    # check response time of under 1 second
    assert response.elapsed.total_seconds() < 1.0
