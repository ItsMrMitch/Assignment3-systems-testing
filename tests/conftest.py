"""pytest fixtures: a fresh Chrome browser per test + automatic screenshots.

pytest reads this file automatically; the fixtures below can be used by any test
simply by naming them as a function argument, e.g. def test_x(driver, logged_in_user).
This use the open-source pytest and Selenium libraries.
"""
import os
import pathlib

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers import DEFAULT_PASSWORD, logout, register_user, text_present, unique_email

# Folder (next to the tests folder) where result screenshots are saved
SHOT_DIR = pathlib.Path(__file__).resolve().parent.parent / "screenshots"


@pytest.fixture
def driver():
    """Start a new Chrome browser for each test and close it afterwards."""
    options = Options()
    if os.getenv("HEADLESS", "1") == "1":      # set HEADLESS=0 to watch the browser
        options.add_argument("--headless=new")   # run Chrome without a visible window
    options.add_argument("--window-size=1440,1000") # fixed size so pages look the same each run
    drv = webdriver.Chrome(options=options)    # Selenium Manager fetches chromedriver
    yield drv    # the test runs here, using this browser
    drv.quit()    # always close the browser when the test ends



@pytest.fixture
def logged_in_user(driver):
    """Register a brand-new account (depends on F1). OpenCart logs the user in."""
    email = unique_email()
    register_user(driver, email)
    # If registration fails, stop here so the real problem (F1) is easy to see
    assert text_present(driver, "Your new account has been successfully created"), "fixture: F1 failed"
    return {"email": email, "password": DEFAULT_PASSWORD}


@pytest.fixture
def registered_user(driver, logged_in_user):
    """Same as logged_in_user, but the session is logged out afterwards."""
    logout(driver)
    return logged_in_user


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot after every test (PASS or FAIL) as evidence for the report."""
    outcome = yield  # let pytest build its normal test report first
    report = outcome.get_result()
    if report.when == "call":  # only the test body itself, not set-up or tear-down
        drv = item.funcargs.get("driver")    # the browser used by this test, if any
        if drv is not None:
            SHOT_DIR.mkdir(exist_ok=True)   # create the screenshots folder if missing
            status = "FAIL" if report.failed else "PASS"
            # File name = test name + result, e.g. test_T001_S1_..._register__PASS.png
            drv.save_screenshot(str(SHOT_DIR / f"{item.name}__{status}.png"))
