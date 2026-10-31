"""helper functions for the LambdaTest eCommerce Playground test suite.

Site under test: https://opencart.abstracta.us (OpenCart 3 demo store).
"""
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Base address of the store; every page is index.php?route=<page>
BASE_URL = "https://opencart.abstracta.us/index.php"
# Password used for every test account we create
DEFAULT_PASSWORD = "Test@12345"
# Maximum seconds to wait for a page element or text before giving up
TIMEOUT = 15


def url(route, **params):
    """Build a site URL, e.g. url('product/search', search='iphone')."""
    # Turn the keyword arguments into "key=value&key2=value2"
    query = "&".join(f"{k}={v}" for k, v in params.items())
    # Add the query string only if there are extra parameters
    return f"{BASE_URL}?route={route}" + (f"&{query}" if query else "")


def unique_email():
    """Return a never-used email address so registration tests can be repeated."""
    # The current time in milliseconds makes every address different
    return f"qa.{int(time.time() * 1000)}@example.com"


def body_text(driver):
    """Return all the visible text on the current page."""
    return driver.find_element(By.TAG_NAME, "body").text


def text_present(driver, text, timeout=TIMEOUT):
    """True if `text` (case-insensitive) appears on the page within `timeout` seconds."""
    try:
        # Keep checking the page text until it contains the wanted text or time runs out
        WebDriverWait(driver, timeout).until(
            lambda d: text.lower() in body_text(d).lower())
        return True
    except TimeoutException:
        # The text never appeared, so the check fails
        return False


def fill(driver, name, value):
    """Clear a form field (located by its name attribute) and type a value."""
    # Wait until the field exists on the page
    el = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, name)))
    el.clear()  # remove anything already in the field
    el.send_keys(value)  # type the new value



def js_click(driver, element):
    """Scroll to an element and click it with JavaScript (avoids overlay problems)."""
    # Scroll so the element is in the middle of the window
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    # A JavaScript click works even if another element is covering the button
    driver.execute_script("arguments[0].click();", element)


def click_xpath(driver, xpath, index=0):
    """Wait for the elements matching an XPath and click the one at `index`."""
    elements = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    js_click(driver, elements[index])


def submit_main_form(driver):
    """Click the submit button of the form inside the main content area."""
    # '#content' is the main page area, so the search box in the page header is ignored
    button = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((
        By.CSS_SELECTOR,
        "#content form input[type='submit'], #content form button[type='submit']")))
    js_click(driver, button)


# ---------------------------------------------------------------- account
def register_user(driver, email, password=DEFAULT_PASSWORD, confirm=None, agree=True):
    """Fill in and submit the registration form (F1)."""
    driver.get(url("account/register"))
    fill(driver, "firstname", "Test")
    fill(driver, "lastname", "User")
    fill(driver, "email", email)
    fill(driver, "telephone", "0412345678")
    fill(driver, "password", password)
    # If no separate confirmation is given, repeat the password (the normal case)
    fill(driver, "confirm", confirm if confirm is not None else password)
    if agree:
        # Tick the Privacy Policy box (required by the site)
        js_click(driver, driver.find_element(By.NAME, "agree"))
    submit_main_form(driver)


def login(driver, email, password):
    """Log in through the login page (F2)."""
    driver.get(url("account/login"))
    fill(driver, "email", email)
    fill(driver, "password", password)
    submit_main_form(driver)


def logout(driver):
    driver.get(url("account/logout"))