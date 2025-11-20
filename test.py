import os

# Define the file structure and content with LATEST updates
files = {
    "requirements.txt": """pytest
pytest-playwright
allure-pytest
pytest-base-url
python-slugify""",

    "Dockerfile": """FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chrome
RUN playwright install-deps
COPY . .
CMD ["pytest", "--alluredir=allure-results"]""",

    "conftest.py": """import pytest
import os
import allure
from playwright.sync_api import Page, sync_playwright
from slugify import slugify

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="https://www.optibet.lv", help="Base URL")
    parser.addoption("--headless-mode", action="store_true", default=True, help="Run headless")

@pytest.fixture(scope="function")
def page(request):
    base_url = request.config.getoption("--base-url")
    headless = request.config.getoption("--headless-mode")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(base_url=base_url)
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshot_name = slugify(item.nodeid)
        try:
            allure.attach(page.screenshot(full_page=True), name=f"Failure: {screenshot_name}", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")""",

    "pages/base_page.py": """import allure
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to {path}")
    def navigate(self, path=""):
        self.page.goto(path)

    @allure.step("Get current URL")
    def get_url(self):
        return self.page.url

    @allure.step("Wait for element {selector} to be visible")
    def wait_for_visible(self, selector):
        self.page.locator(selector).wait_for(state="visible")""",

    "pages/home_page.py": """import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.logo = "a[href='/']"
        self.menu_casino = "a[data-role='Casino']"
        self.menu_sports = "a[data-role='Sportsbook']"
        self.lang_switcher = "[class*='language-menu__label']"
        self.lang_option_ru = "a[data-id='langMenuItem-ru']"
        self.lang_option_lv = "a[data-id='langMenuItem-lv']"
        self.lang_option_en = "a[data-id='langMenuItem-en']"
        self.active_lang_display = "[class*='language-menu__label']"

    @allure.step("Verify Header Elements are visible")
    def verify_header_elements(self):
        expect(self.page.locator(self.logo).first).to_be_visible()
        expect(self.page.locator(self.menu_casino)).to_be_visible()
        expect(self.page.locator(self.menu_sports)).to_be_visible()

    @allure.step("Switch language to {language_code}")
    def switch_language(self, language_code):
        self.page.click(self.lang_switcher)
        if language_code == "RU": self.page.click(self.lang_option_ru)
        elif language_code == "LV": self.page.click(self.lang_option_lv)
        elif language_code == "EN": self.page.click(self.lang_option_en)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Verify active language is {expected_lang}")
    def verify_active_language(self, expected_lang):
        expect(self.page.locator(self.active_lang_display)).to_have_text(expected_lang.lower(), ignore_case=True)
        current_url = self.get_url()
        if expected_lang.lower() != "lv":
            assert f"/{expected_lang.lower()}" in current_url""",

    "pages/promotions_page.py": """import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class PromotionsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/promotions"
        self.promo_cards = "a[data-role='promotion']" 
        self.filter_casino = "button:has-text('Kazino')" 
        self.filter_sports = "button:has-text('Sports')"
        self.card_title = "[data-role='promotionTitle']"
        self.read_more_link = "[data-role='promotionTitleLink']"

    @allure.step("Navigate to Promotions Page")
    def open(self):
        self.navigate(self.url_path)

    @allure.step("Filter promotions by {category}")
    def filter_by(self, category):
        try:
            if category == "Casino": self.page.click(self.filter_casino)
            elif category == "Sports": self.page.click(self.filter_sports)
        except:
            print(f"Could not click filter {category}, checking list anyway.")
        self.page.wait_for_timeout(1000)

    @allure.step("Verify promotion cards are displayed and valid")
    def verify_promotions_list(self):
        try:
            self.page.wait_for_selector(self.promo_cards, timeout=5000)
        except:
            pass 
        count = self.page.locator(self.promo_cards).count()
        assert count > 0, "No promotion cards found!"
        for i in range(min(count, 3)):
            card = self.page.locator(self.promo_cards).nth(i)
            expect(card).to_be_visible()
            expect(card.locator(self.card_title)).to_be_visible()
            expect(card.locator(self.read_more_link)).to_be_visible()""",

    "pages/registration_page.py": """import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/registration"
        self.reg_button_header = "header button:has-text('Sign up')"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.submit_btn = "button[type='submit']"
        self.email_error = "text=valid email" 
        self.password_error = "text=password"

    @allure.step("Open Registration Form")
    def open_registration_form(self):
        self.navigate()
        self.page.click(self.reg_button_header)
        self.wait_for_visible(self.email_input)

    @allure.step("Verify main fields presence")
    def verify_fields_present(self):
        expect(self.page.locator(self.email_input)).to_be_visible()
        expect(self.page.locator(self.password_input)).to_be_visible()
        expect(self.page.locator(self.submit_btn)).to_be_visible()

    @allure.step("Fill registration form")
    def fill_form(self, email, password):
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)

    @allure.step("Submit form")
    def submit(self):
        self.page.click(self.submit_btn)

    @allure.step("Verify email error is shown")
    def verify_email_error(self):
        expect(self.page.locator(self.email_error).first).to_be_visible()

    @allure.step("Verify password error is shown")
    def verify_password_error(self):
        expect(self.page.locator(self.password_error).first).to_be_visible()""",

    "pages/login_page.py": """import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login_header_btn = "header button:has-text('Login')"
        self.username_input = "[data-role='loginEmailInput']"
        self.password_input = "[data-role='password']"
        self.login_submit_btn = "[data-role='loginSubmit']"
        self.login_error_msg = "[data-role='validationError']"

    @allure.step("Open Login Form")
    def open_login_modal(self):
        self.navigate()
        self.page.click(self.login_header_btn)

    @allure.step("Login with credentials")
    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_submit_btn)

    @allure.step("Verify login failure message")
    def verify_login_failed(self):
        error_elem = self.page.locator(self.login_error_msg)
        expect(error_elem).to_be_visible()
        expect(error_elem).to_contain_text("The username or password is incorrect")""",

    "tests/test_scenarios.py": """import pytest
import allure
from pages.home_page import HomePage
from pages.promotions_page import PromotionsPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

@allure.feature("Header Navigation")
@allure.story("Language Switcher")
@allure.severity(allure.severity_level.CRITICAL)
def test_header_language_switching(page):
    home = HomePage(page)
    home.navigate()
    home.verify_header_elements()
    home.switch_language("LV")
    home.verify_active_language("LV")
    home.switch_language("EN")
    home.verify_active_language("EN")

@allure.feature("Promotions")
@allure.story("Filter Promotions")
def test_promotions_filtering(page):
    promo_page = PromotionsPage(page)
    promo_page.open()
    promo_page.filter_by("Casino")
    promo_page.verify_promotions_list()
    promo_page.filter_by("Sports")
    promo_page.verify_promotions_list()

@allure.feature("Registration")
@allure.story("Registration Validation (Negative)")
@pytest.mark.parametrize("email, password, error_type", [
    ("test_without_at.com", "ValidPass123!", "email"),
    ("valid@email.com", "123", "password"),
])
def test_registration_validation(page, email, password, error_type):
    reg_page = RegistrationPage(page)
    reg_page.open_registration_form()
    reg_page.verify_fields_present()
    reg_page.fill_form(email, password)
    reg_page.submit()
    if error_type == "email": reg_page.verify_email_error()
    elif error_type == "password": reg_page.verify_password_error()

@allure.feature("Authentication")
@allure.story("Login Negative Test")
def test_login_negative(page):
    login_page = LoginPage(page)
    login_page.open_login_modal()
    login_page.login("non_existent_user@fake.com", "WrongPass123!")
    login_page.verify_login_failed()""",
    
    "README.md": """# Optibet Automation Test

## Setup
1. Create venv: `python -m venv venv`
2. Activate: `venv\\Scripts\\activate` (Windows) or `source venv/bin/activate` (Mac)
3. Install: `pip install -r requirements.txt`
4. Install Browsers: `playwright install`

## Run
`pytest --alluredir=allure-results`
"""
}

# Create directories
os.makedirs("pages", exist_ok=True)
os.makedirs("tests", exist_ok=True)

# Write files
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Created {filepath}")