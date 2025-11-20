import allure
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to {path}")
    def navigate(self, path=""):
        self.page.goto(path, wait_until="domcontentloaded")
        self.handle_cookies()

    @allure.step("Handle Cookie Banner")
    def handle_cookies(self):
        try:
            cookie_btn = self.page.locator("#CookiebotDialogBodyLevelButtonLevelOptinAllowAll, button:has-text('Akceptēt'), button:has-text('Accept')")
            if cookie_btn.count() > 0 and cookie_btn.first.is_visible():
                cookie_btn.first.click()
        except:
            pass

    @allure.step("Get current URL")
    def get_url(self):
        return self.page.url

    @allure.step("Wait for element {selector} to be visible")
    def wait_for_visible(self, selector):
        self.page.locator(selector).first.wait_for(state="visible")