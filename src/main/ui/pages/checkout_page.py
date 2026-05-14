from playwright.sync_api import Page, expect


class CheckoutPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.product_prices = page.locator(".inventory_item_price")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator('[data-test="error"]')

    def open_checkout(self):
        self.page.locator('[data-test="checkout"]').click()

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Zip/Postal Code").fill(zip_code)
        self.page.locator('[data-test="continue"]').click()

    def get_success_text(self):
        return self.page.locator('.complete-header').inner_text()

    def get_item_total_price(self):
        prices_text = self.product_prices.all_text_contents()
        prices = [float(p.replace("$", "")) for p in prices_text]
        tax_text = self.page.locator("[data-test='tax-label']").inner_text()
        tax = float(tax_text.split('$')[1])
        expected_total = sum(prices) + tax
        return expected_total

    def get_item_total_price_after_continue(self):
        total_price_text = self.page.locator("[data-test='total-label']").inner_text()
        total_price = float(total_price_text.split('$')[1])
        return total_price

    def start_checkout(self):
        expected_total = self.get_item_total_price()
        total_price = self.get_item_total_price_after_continue()

        assert total_price == expected_total

        self.page.locator('[data-test="finish"]').click()
        assert self.get_success_text() == "Thank you for your order!"