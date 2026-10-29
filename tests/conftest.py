"""pytest fixtures: a fresh Chrome browser per test + automatic screenshots."""
import os
import pathlib

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers import DEFAULT_PASSWORD, logout, register_user, text_present, unique_email

SHOT_DIR = pathlib.Path(__file__).resolve().parent.parent / "screenshots"


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "1") == "1":      # set HEADLESS=0 to watch the browser
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    drv = webdriver.Chrome(options=options)    # Selenium Manager fetches chromedriver
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_user(driver):
    """Register a brand-new account (depends on F1). OpenCart logs the user in."""
    email = unique_email()
    register_user(driver, email)
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
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        drv = item.funcargs.get("driver")
        if drv is not None:
            SHOT_DIR.mkdir(exist_ok=True)
            status = "FAIL" if report.failed else "PASS"
            drv.save_screenshot(str(SHOT_DIR / f"{item.name}__{status}.png"))
