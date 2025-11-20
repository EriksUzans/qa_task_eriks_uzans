import allure
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
        self.wait_for_visible(self.menu_casino)
        expect(self.page.locator(self.logo).first).to_be_visible()
        expect(self.page.locator(self.menu_casino)).to_be_visible()
        expect(self.page.locator(self.menu_sports)).to_be_visible()

    @allure.step("Switch language to {language_code}")
    def switch_language(self, language_code):
        self.handle_cookies()
        self.wait_for_visible(self.lang_switcher)
        self.page.click(self.lang_switcher)
        if language_code == "RU": self.page.click(self.lang_option_ru)
        elif language_code == "LV": self.page.click(self.lang_option_lv)
        elif language_code == "EN": self.page.click(self.lang_option_en)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)

    @allure.step("Verify active language is {expected_lang}")
    def verify_active_language(self, expected_lang):
        expect(self.page.locator(self.active_lang_display)).to_have_text(expected_lang.lower(), ignore_case=True)
        current_url = self.get_url()
        if expected_lang.lower() != "lv":
            assert f"/{expected_lang.lower()}" in current_url