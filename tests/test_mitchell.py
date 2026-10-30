"""Member 1 - F1 User Registration (T001), F2 User Login (T002), F11 Forgotten Password (T003)."""
from helpers import (DEFAULT_PASSWORD, fill, login, logout, register_user,
                     submit_main_form, text_present, unique_email, url)


# ===== T001 - F1 User Registration ========================================
def test_T001_S1_register_valid_new_user(driver):
    # Valid details + a never-used email -> account is created
    register_user(driver, unique_email())
    assert text_present(driver, "Your new account has been successfully Created")


def test_T001_S2_register_duplicate_email(driver):
    # Register once, log out, then try to register again with the same email
    email = unique_email()
    register_user(driver, email)
    logout(driver)
    register_user(driver, email)
    assert text_present(driver, "E-Mail Address is already registered")


def test_T001_S3_register_password_mismatch(driver):
    # Password confirmation differs from the password -> validation error
    register_user(driver, unique_email(), confirm="Different@999")
    assert text_present(driver, "Password confirmation does not match password")


# ===== T002 - F2 User Login ===============================================

def test_T002_S1_login_valid_credentials(driver, registered_user): # Depends on F1: the account is created by the fixture
    login(driver, registered_user["email"], registered_user["password"])
    assert "account/account" in driver.current_url
    assert text_present(driver, "My Account")

def test_T002_S2_login_wrong_password(driver, registered_user):
    login(driver, registered_user["email"], "WrongPass#1")
    assert text_present(driver, "No match for E-Mail Address and/or Password")

def test_T002_S3_login_unregistered_email(driver):
    login(driver, unique_email(), DEFAULT_PASSWORD)
    assert text_present(driver, "No match for E-Mail Address and/or Password")
