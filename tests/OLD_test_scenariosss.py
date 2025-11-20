import pytest
import allure
from playwright_stealth import Stealth
from utils.data_factory import UserDataFactory

from pages.home_page import HomePage
from pages.promotions_page import PromotionsPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

def apply_stealth(page):
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

@allure.feature("Header Navigation")
@allure.story("Language Switcher")
@allure.severity(allure.severity_level.CRITICAL)
def test_header_language_switching(page):
    apply_stealth(page)
    home = HomePage(page)
    print("STEP: HomePage initialized")
    
    home.navigate()
    print(f"STEP: Navigated to {page.url}")
    
    home.verify_header_elements()
    print("STEP: Header elements (Logo, Menu) verified")
    
    home.switch_language("RU")
    print("STEP: Switched language to RU")
    home.verify_active_language("RU")
    print("STEP: Verified active language is RU")

    home.switch_language("LV")
    print("STEP: Switched language to LV")
    home.verify_active_language("LV")
    print("STEP: Verified active language is LV")

    home.switch_language("EN")
    print("STEP: Switched language to EN")
    home.verify_active_language("EN")
    print("STEP: Verified active language is EN")

    home.switch_language("RU")
    print("STEP: Switched language back to RU")
    home.verify_active_language("RU")
    print("STEP: Verified active language restored to RU")

@allure.feature("Promotions")
@allure.story("Filter Promotions")
def test_promotions_filtering(page):
    apply_stealth(page)
    promo_page = PromotionsPage(page)
    
    promo_page.open()
    print("1. Navigated to Promotions page")

    promo_page.verify_promotions_list()
    print("2. Verified list visibility and content")
    
    categories = ["Casino", "Sports"]
    for category in categories:
        promo_page.filter_by(category)
        print(f"3. Applied filter: {category}")
        
        promo_page.verify_promotions_list()
        print(f"4. Verified list content for {category}")
        
    promo_page.verify_detailed_page()
    print("5. Verified detailed page title and description")

@allure.feature("Registration")
@allure.story("Registration Validation (Negative)")
@pytest.mark.parametrize("email, password, error_type", [
    # Scenario 1: Faker used for invalid email
    (UserDataFactory.get_invalid_email(), UserDataFactory.get_valid_password(), "email"),
    
    # Scenario 2: Faker used for weak password (valid email + weak pass)
    (f"valid_{UserDataFactory.get_invalid_email()}@gmail.com", UserDataFactory.get_weak_password(), "password"),
    
    # Scenario 3: Empty required field (Explicit None)
    (None, UserDataFactory.get_valid_password(), "empty")
])
def test_registration_validation(page, email, password, error_type):
    apply_stealth(page)
    print(f"TEST DATA GENERATED: Email='{email}', Password='{password}'")
    
    reg_page = RegistrationPage(page)
    reg_page.open_registration_form()
    print("form opened")
    
    reg_page.verify_fields_present()
    print("verified field presence")
    
    reg_page.fill_form(email, password)
    print(f"form filled")
    
    reg_page.submit()
    
    if error_type == "email": 
        reg_page.verify_email_error()
        print("email error verified")
    elif error_type == "password": 
        reg_page.verify_password_error()
        print("password error verified")
    elif error_type == "empty":
        reg_page.verify_empty_field_error()
        print("empty field error verified")

@allure.feature("Authentication")
@allure.story("Login Negative Test")
def test_login_negative(page):
    apply_stealth(page)
    home = HomePage(page)
    home.navigate()
    page.reload()
    home.switch_language("EN")
    login_page = LoginPage(page)
    login_page.open_login_modal()
    login_page.login("non_existent_user@fake.com", "WrongPass123!")
    login_page.verify_login_failed()