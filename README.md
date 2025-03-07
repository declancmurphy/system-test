# Introduction

This framework aims to test two platforms: SweetShop (https://sweetshop.netlify.app/) and AirportGap (https://airportgap.com/). 

Example reports have been included in the "/docs" folder, which should provide an idea of the expected format this framework yields with regards to test execution reporting. By default, test runs should yield reporting from pytest-html in the form of "log.html" files within "/reports". The next time a test is executed (i.e. "run.sh" is invoked), the previous results are moved into "/report_archive". These directories are included in .gitignore and should serve as temporary local results.

Also included is a working document called "known_issues.md" which serves to track current issues across all platforms this framework tests. Note that given the limited time, this is not an exhaustive list of issues and a list of improvements has been constructed to enhance the general infrastructure, test capability and framework quality (see "Improvements").

At the root of the directory should be everything needed to setup and invoke the framework (prepare.sh, run.sh, docker, docs etc).

This framework has been built with the assumption that it would be utilised by pipeline runners, of which most commonly are running a debian-based OS like Ubuntu. Considering this, the framework has been built using a Ubuntu 22.04 image and relies on Docker for containerisation.

Tests are divided and structured on a per-platform basis under "/tests" and tests are grouped under functional areas or types in "test_*.py" files (following pytest convention).

# SETUP

Given the assumptions made, this framework assumes you are running a debian-OS like Ubuntu 22.04, if needed, download an iso from here and setup a VM using your desired virtualisation technology: https://releases.ubuntu.com/jammy/

For windows users, some options to setup and run this framework include the following:
1) Clone this repo into a VM running any stable linux distro (e.g. Ubuntu 22.04.2 LTS: https://ubuntu.com/download/desktop/thank-you?version=24.04.2&architecture=amd64&lts=true)
2) Install Docker Desktop (requires subscription), or Moby (open-source)

Getting started:

Clone the repo: https://github.com/<>.git

Installation of necessary pre-requisites is performed automatically by the `prepare.sh` script - BEWARE THAT THIS WILL ATTEMPT TO MODIFY YOUR MACHINE (install docker etc).
```
    sudo ./prepare.sh
```

## Configuration

A templated '.env' file has been supplied to provide an example of the current capability to configure the framework for different modes of operation. 

Example parameters that can be tweaked include headless mode, default browser for UI test execution, keep container alive for debug and switching between local and containerised test execution.

# Running tests

`run.sh` is the top-level script which prepares the test environment and executes tests. 

Provide 'run.sh' with executable permissions by using ```chmod -R +x run.sh```.

### Changing browser type:

The default browser type used for testing UI applications is Chrome in headless mode.

The dependencies for this are defined in the dockerfile and the use of chrome is explicitly defined in the Selenium WebDriver setup fixture in sweet_utils.py.

A note has been made about improvements for multi-browser support in the "Improvements" section of this README.

## Troubleshooting:

It is often useful to run tests in headful mode when troubleshooting failures with UI test execution. To enable visibility of the UI and actions executed, disable headless mode by adding the argument "HEADLESS=0" to your .env file. This can be used while having "LOCAL=1" or "LOCAL=0", as the container display can be forwarded to the host using x11/Xorg.

One common issue can be found with XOrg not starting properly on the host machine, it is sometimes useful to restart your display manager and check XOrg is running with:
```
ps aux | grep Xorg
```

# APPROACH

Technology Stack:

At a high level, the following are used to test SweetShop and AirportGap (see "apt_dependencies.txt" for a comprehensive list of libraries used):

- Docker
- Python
- Selenium WebDriver / Selenium Library
- Pytest
- Requests
- Bash

Given the limited time to create this project, the focus has been on positive user flow tests, general framework infrastructure and potential for test cability. Please see notes in "Improvements" on potential improvements to framework infrastrcut Specifically, because the functionality on SweetShop is so broken, more emphasis has been placed on fleshing out the "airportgap" suite. 

As the dependencies and more generally, the framework isn't currently too large, I have gone with the approach of containerising the core framework dependencies and including a pre-built selenium-chrome image (serving Selenium Grid in standalone mode, which is pointed at by our webdriver fixture) to ensure consistency across environments and optimise for pipeline execution. Mounting the tests directory in ensures we can retest changes efficiently without having to rebuilt docker layers. 

## SweetShop:

The pages directory to offers a Page Object Model (POM), a standard design approach used for the benefits of future-proofing the framework, allowing for ease of test development and maintenance, reducing also the possibility of duplication across tests. If changes are made to the UI, this can easily be addressed in a centralised location, rather than having to address changes in individual test files. Each page has a dedicated file offering a class for that page, constructing variables and methods unique to those pages. 
A base class is defined in "base_page.py", which the other page classes inherit and expand upon. Locators and page-specific actions should be defined in each page class. I have mostly tried to define the method of which selenium webdriver will identify elements based on site accessibility restrictions (e.g. some elements are accessible enough to use id, some need xpath.)
Page classes should be instantiated as objects to use in tests for the purpose of performing defined actions and utilising defined locators and URLs built using the BasePage class.

I have tried to display multiple ways of covering test pathways, e.g. having "expected_result" values in "login_data.json" that are ingested by "test_login()" to assertain outcomes accordingly, having assertations and error handling naturally handle invalid test data (see invalid product in "products.json" and handling for this in "product_page.add_product_to_basket") and explicity test cases to cover positive/negative tests (see test_valid_checkout_form_data vs test_invalid_checkout_form_data_email). Given more time I would add more independent test cases to check invalid/negative pathways and edge cases, potentially placing more emphasis on test cases covering known issues.

I have generally tried to go with a data-driven approach to parameterise test cases, using defined json objects (in /test_data).

Generally, I spent less time focusing on test capability on this platform given the website is intentionally broken. Whilst I agree it is benefecial to implement a shift-left test strategy, I think until the core functionality highlighted in known_issues.md is addressed, efforts are somewhat wasted as assertations and the showcased POM will be inaccurate if built before the site functionality. However, I have set up some examples of assertations and tests for implemented functionality, just keep in mind observed test failures are purposeful (to demonstrate potential assertations).

Also included is fixture inheritance, shown through a setup fixture within "test_basket.py", using general setup and teardown steps used in most basket operation tests. Note that I have used yield as part of this fixture to ensure we can teardown each test by clearing the basket (as a product is added to the basket), even though some of the tests will attempt to do this already.

## AirportGap:

As already explained, most of the focus of testing is around covering positive pathways for all endpoints. Basic non-functional tests have been included in the "/test_non_functional.py" test file.

Similarly to SweetShop, i have constructed test data in json format to allow easy declaration of test data and seperate this from the other suite files. I have limited these test data sets to reduce the number of parameterised test runs for showcase purposes.

A useful setup/teardown fixture for requests made to the "/favorites" endpoint has been created.

One authentication token has been pre-generated and hardcoded, indicated in "users.json", this is used in all tests hitting endpoints that require authentication (see note here in "Improvements").

I have used the pytest-order to make sure rate limit testing happen last, so as to not affect other tests.

# FUTURE IMPROVEMENTS

The below lists areas for improvement given available time to expand the framework capability.

## Configuration


Utilising pytest.ini and other useful configuration files to abstract configuration items included at a more granular level, e.g. control of logging, suite variables etc and more importantly, pytest-specific configuration items like test directory scope, markers etc.

## Containerisation: 

    Configure args for run.sh to allow options like --no-cache for rebuilding containers without caching etc. (currently done via .env)
    Improve cache/layer management as framework scales to ensure layers are kept to a minimal, especially if build time increases and happens more often, reducing pipeline compute.

### SweetShop:

- Flesh out the rest of tests, assuming site functionality is to be added/fixed:
    - add locator checks (error handling for visibility, element enabling etc)
    - add more tests, concrete assertations given correct functionality, e.g:
        Checkout with empty basket
        Empty basket from account page
        More user login permutations (once user DB implemented)
        Non-functional auth tests, e.g. password throttling

- Improve error handling for every POM method (e.g. attempts to navigate to pages)
- Add useful messaging to assertations
- Improve selenium command usage (rather than using go-to functions/quick wins, make steps more robust i.e. waiting for elements before clicking)

### AirportGap:

General:
- Add negative tests for each endpoint - testing invalid methods, invalid IDs (for those that accept)
- Expand test data and define test data fixtures (e.g. more users with and without tokens, large data set for distances)
- Generate authentication token on-the-fly rather than hard-coded
- Add assertations for improved status code checking and more granular response data/json checks
- Better error handling for each request type
- Testing invalid request structures (to trigger 422 status codes etc)
- Counters for tests run and requests made per run to reduce load test setup wait time
- Add messaging to assertations
- Tests for auth bypass on all endpoints that require based on dictionaries
- SQL Injection tests on all endpoints
- Add stress tests and use a tool like locust.io for load testing for scalability given future framework scope increase

## Environment support 

Using poetry/virtual environment to manage dependencies, rather than current approach of using "prepare.sh" - once the framework expands and requires more dependencies, it would be easier to manage versions, dependency conflicts and general environment stability using poetry.

Given the framework current tailors towards linux/debian OS, it would be beneficial to adapt to macOS/Windows systems, possibly with the help of infrastructure-as-code tools like Packer/Ansible/Vagrant, as the framework has some reliance on Docker. WSL could help to find a containerised solution for Windows.

As a representative system, ideally this would be integrated into a pipeline system. The work required to integrate this framework into CI would not be extensive, for example for GitHub actions, a ci.yml could be created defining each job (most likely split into a job for each platform), using the environment variables defined in ".env" to auto-install dependencies. As the systems under test do not have any extensive host requirements, there is not a huge need for infra-as-code tools.

## Improved reporting

Currently, the framework uses the reporting package "pytest-html" for basic reporting and while this is generally enough in a lot of basic test systems, there is potential to improve the reporting by doing using tools like "allure-pytest", improving logging, readability and integrating with appropriate test management systems like Jira/Xray or TestRail for test coverage traceability.

## Multi-browser test support

Currently, this framework only allows the use of chrome. However, it would be useful and not difficult to add capability for other common browser, such as edge and firefox.

Most of this work would be done by either allowing an environment variable to select a specific browser to run tests on, or using "ALL" to run the specified tests on all browser types.

One change that would need to happen for each test environment is to the driver setup fixture in conftest.py, as currently this explicitly calls webdriver.Chrome. This can be managed with an environment variable.

### For containerised testing:
This would also require defined services specified in docker-compose.yml for each additional browser type and each browser added under the "depends-on:" tag for the test-runner. Essentially, you'd have a Selenium Grid Standalone server served by each service with a unique address or port, which the test executor ("test-runner" in the case of this framework) could send commands to execute on.

### For local testing:
The dependencies for each browser will need to be managed in the same fashion (manually), or via poetry as explained above.