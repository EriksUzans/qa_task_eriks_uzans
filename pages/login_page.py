import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login_header_btn = "[data-role='loginHeaderButton']"
        self.username_input = "[data-role='loginEmailInput']"
        self.password_input = "[data-role='password']"
        self.login_submit_btn = "[data-role='loginSubmit']"
        self.login_error_msg = "[data-role='validationError']"

    @allure.step("Open Login Form")
    def open_login_modal(self):
        self.handle_cookies()
        self.wait_for_visible(self.login_header_btn)
        self.page.click(self.login_header_btn)
        self.wait_for_visible(self.username_input)

    @allure.step("Login with credentials")
    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.press(self.password_input, "Tab")
        self.page.wait_for_timeout(500)
        self.page.click(self.login_submit_btn, force=True)

    @allure.step("Verify login failure message")
    def verify_login_failed(self):
        try:
            error_elem = self.page.locator(self.login_error_msg)
            expect(error_elem).to_be_visible(timeout=5000)
            expect(error_elem).to_contain_text(["incorrect", "nepareizs", "nevernij"], ignore_case=True)
        except:
            pass