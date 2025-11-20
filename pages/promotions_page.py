import allure
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
        
        # Updated selectors for detailed page
        self.detail_main_title = ".main-title-OB"
        self.detail_section_desc = ".section_description-top"

    @allure.step("Navigate to Promotions Page")
    def open(self):
        self.navigate(self.url_path)
        self.page.wait_for_load_state("networkidle") 

    @allure.step("Filter promotions by {category}")
    def filter_by(self, category):
        try:
            if category == "Casino": self.page.click(self.filter_casino)
            elif category == "Sports": self.page.click(self.filter_sports)
            self.page.wait_for_timeout(1000)
        except:
            pass

    @allure.step("Verify promotion cards are displayed and valid")
    def verify_promotions_list(self):
        try:
            self.page.wait_for_selector(self.promo_cards, timeout=15000)
        except:
            pass
            
        count = self.page.locator(self.promo_cards).count()
        assert count > 0, "No promotion cards found!"
        
        # Use .first to avoid strict mode errors
        card = self.page.locator(self.promo_cards).first
        expect(card).to_be_visible()
        expect(card.locator(self.card_title)).to_be_visible()
        expect(card).to_be_visible()
        
    @allure.step("Verify detailed page opens")
    def verify_detailed_page(self):
        first_card = self.page.locator(self.promo_cards).first
        first_card.click()
        self.page.wait_for_load_state("domcontentloaded")
        
        assert "/promotion/" in self.page.url or "/piedavajumi/" in self.page.url
        
        try:
            expect(self.page.locator(self.detail_main_title).first).to_be_visible()
            expect(self.page.locator(self.detail_section_desc).first).to_be_visible()
        except:
            expect(self.page.locator("h1").first).to_be_visible()
            
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")