from playwright.sync_api import Page, expect

from src.main.ui.utils.constansts import Urls


class CheckoutPage:
    URL = Urls.BASE

    def __init__(self, page: Page):
        self.page = page
        self.product_prices = page.locator(".inventory_item_price")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")

    def open_checkout(self):
        self.page.locator('[data-test="checkout"]').click()
        expect(self.page.locator("[data-test='title']")).to_have_text("Checkout: Your Information")

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Zip/Postal Code").fill(zip_code)
        self.page.locator('[data-test="continue"]').click()

    def get_success_text(self):
        return self.page.locator('.complete-header').inner_text()

    def get_item_total_price_after_checkout(self):
        total_price_text = self.page.locator("[data-test='subtotal-label']").inner_text()
        total_price = float(total_price_text.split('$')[1])
        return total_price

    def finish_checkout(self):
        self.finish_button.click()