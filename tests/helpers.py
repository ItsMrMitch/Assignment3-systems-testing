"""helper functions for the LambdaTest eCommerce Playground test suite.

Site under test: https://opencart.abstracta.us (OpenCart 3 demo store).
"""
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE_URL = "https://opencart.abstracta.us/index.php"
DEFAULT_PASSWORD = "Test@12345"
TIMEOUT = 15


def url(route, **params):
    """Build a site URL, e.g. url('product/search', search='iphone')."""
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{BASE_URL}?route={route}" + (f"&{query}" if query else "")


def unique_email():
    """Return a never-used email address so registration tests can be repeated."""
    return f"qa.{int(time.time() * 1000)}@example.com"


def body_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text


def text_present(driver, text, timeout=TIMEOUT):
    """True if `text` (case-insensitive) appears on the page within `timeout` seconds."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: text.lower() in body_text(d).lower())
        return True
    except TimeoutException:
        return False


def fill(driver, name, value):
    """Clear a form field (located by its name attribute) and type a value."""
    el = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, name)))
    el.clear()
    el.send_keys(value)


def js_click(driver, element):
    """Scroll to an element and click it with JavaScript (avoids overlay problems)."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)


def click_xpath(driver, xpath, index=0):
    """Wait for the elements matching an XPath and click the one at `index`."""
    elements = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    js_click(driver, elements[index])


def submit_main_form(driver):
    """Click the submit button of the form inside the main content area."""
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
    fill(driver, "confirm", confirm if confirm is not None else password)
    if agree:
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