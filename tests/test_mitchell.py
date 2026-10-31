"""Member 1 - F1 User Registration (T001), F2 User Login (T002), F11 Forgotten Password (T003).
driver arguement is a fresh chrome browser created by confest.py
"""
from helpers import (DEFAULT_PASSWORD, fill, login, logout, register_user,
                     submit_main_form, text_present, unique_email, url)


# ===== T001 - F1 User Registration ========================================
def test_T001_S1_register_valid_new_user(driver):
     # Scenario 1 (success): valid details and an email that has never been used
    register_user(driver, unique_email()) # fills in and submits the registration form
    # The site should confirm the account was created
    assert text_present(driver, "Your new account has been successfully Created")


def test_T001_S2_register_duplicate_email(driver):
    # Scenario 2 (failure): registering with an email that already has an account
    email = unique_email()  # one email used for both registrations
    register_user(driver, email)  # first registration creates the account
    logout(driver)   # leave the account so the form can be used again
    register_user(driver, email)   # second registration reuses the same email
    # The site should refuse and warn that the email is already registered
    assert text_present(driver, "E-Mail Address is already registered")


def test_T001_S3_register_password_mismatch(driver):
    # Scenario 3 (failure): the password confirmation differs from the password
    register_user(driver, unique_email(), confirm="Different@999")
    # The site should show a validation error and NOT create the account
    assert text_present(driver, "Password confirmation does not match password")


# ===== T002 - F2 User Login ===============================================

def test_T002_S1_login_valid_credentials(driver, registered_user): 
    # Scenario 1 (success): the account is created by the registered_user fixture
    # (this is the dependency on F1), then we log in with its correct details
    login(driver, registered_user["email"], registered_user["password"])
    # A successful login lands on the My Account page
    assert "account/account" in driver.current_url
    assert text_present(driver, "My Account")

def test_T002_S2_login_wrong_password(driver, registered_user):
    # Scenario 2 (failure): correct email but the wrong password
    login(driver, registered_user["email"], "WrongPass#1")
    # The site should reject the login with a warning message
    assert text_present(driver, "No match for E-Mail Address and/or Password")

def test_T002_S3_login_unregistered_email(driver):
    # Scenario 3 (failure): an email address that has never been registered
    login(driver, unique_email(), DEFAULT_PASSWORD)
    # The site gives the same warning as for a wrong password
    assert text_present(driver, "No match for E-Mail Address and/or Password")

# ===== T003 - F11 Forgotten Password ======================================

def request_reset(driver, email):
    # Helper for T003: open the forgotten-password page, enter an email and submit
    driver.get(url("account/forgotten"))
    fill(driver, "email", email)
    submit_main_form(driver)

def test_T003_S1_reset_registered_email(driver, registered_user):
    # Scenario 1 (success): an email that belongs to a registered account
    request_reset(driver, registered_user["email"])
    # The site should say a reset link has been sent
    assert text_present(driver, "confirmation link")

def test_T003_S2_reset_unregistered_email(driver):
    # Scenario 2 (failure): a well-formed email that has no account
    request_reset(driver, unique_email())
    # The site should warn that the email was not found in its records
    assert text_present(driver, "was not found")

def test_T003_S3_reset_malformed_email(driver):
    # Scenario 3 (failure): text that is not an email address at all
    request_reset(driver, "not-an-email") 
    # Malformed input must never produce the success message
    # (we check that the "reset link sent" text does NOT appear within 3 seconds)
    assert not text_present(driver, "confirmation link", timeout=3)