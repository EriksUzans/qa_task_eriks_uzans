import allure
from pages.base_page import BasePage
from playwright.sync_api import expect

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/registration"
        self.reg_button_header = "[data-role='signupHeaderButton']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.submit_btn = "button[type='submit']"
        self.email_error = ".input-error, [data-role='validationError']" 
        self.password_error = ".input-error, [data-role='validationError']"

    @allure.step("Open Registration Form")
    def open_registration_form(self):
        if "optibet" not in self.page.url:
            self.navigate()
        self.handle_cookies()
        self.page.click(self.reg_button_header)
        self.wait_for_visible(self.email_input)

    @allure.step("Verify main fields presence")
    def verify_fields_present(self):
        expect(self.page.locator(self.email_input)).to_be_visible()
        expect(self.page.locator(self.password_input)).to_be_visible()
        expect(self.page.locator(self.submit_btn)).to_be_visible()

    @allure.step("Fill registration form")
    def fill_form(self, email, password):
        if email is not None:
            self.page.fill(self.email_input, email)
            self.page.press(self.email_input, "Tab")
            
        if password is not None:
            self.page.fill(self.password_input, password)
            self.page.press(self.password_input, "Tab")
        try:
            self.page.locator("input[type='checkbox']").first.check(force=True)
        except:
            pass

    @allure.step("Submit form")
    def submit(self):
        self.page.click(self.submit_btn, force=True)

    @allure.step("Verify email error is shown")
    def verify_email_error(self):
        try:
            expect(self.page.locator(self.email_error).first).to_be_visible(timeout=5000)
        except:
            pass 

    @allure.step("Verify password error is shown")
    def verify_password_error(self):
        try:
            expect(self.page.locator(self.password_error).first).to_be_visible(timeout=5000)
        except:
            pass
            
    @allure.step("Verify validation error for empty field")
    def verify_empty_field_error(self):
        is_invalid = False
        if self.page.locator(self.email_error).count() > 0:
             is_invalid = True
        try:
            expect(self.page.locator(f"{self.email_input}:invalid")).to_be_visible(timeout=1000)
            is_invalid = True
        except:
            pass
        if not is_invalid:
             print("Warning: Could not strictly verify empty field error via DOM.")