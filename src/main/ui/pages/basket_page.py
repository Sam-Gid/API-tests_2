from playwright.sync_api import Page, expect


class BasketPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.item_cards = page.locator(".cart_item")

    def open_cart(self):
        self.page.locator(".shopping_cart_link").click()

    def expect_item_in_cart(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        expect(card).not_to_be_visible()

    def get_item_names(self):
        return self.item_cards.locator(".inventory_item_name").all_text_contents()

    def get_item_prices(self):
        prices_text = self.item_cards.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices_text]

    def get_item_total_price(self):
        prices_text = self.item_cards.locator(".inventory_item_price").all_text_contents()
        return sum(float(p.replace("$", "")) for p in prices_text)

    def remove_from_cart(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        button = card.locator("button")
        button.click()


