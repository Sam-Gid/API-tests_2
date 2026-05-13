from playwright.sync_api import Page, expect


class BasketPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator(".inventory_item")
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.locator("#login-button")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_button = page.locator('[data-test="continue"]')

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def add_to_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Add to cart":
            button.click()
        return button

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def open_cart(self):
        self.page.locator(".shopping_cart_link").click()

    def remove_from_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Remove":
            button.click()
        return button

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Zip/Postal Code").fill(zip_code)
        self.continue_button.click()

    def checkout_info(self):
        prices_text = self.page.locator(".inventory_item_price").all_text_contents()
        prices = [float(p.replace("$", "")) for p in prices_text]
        tax_text = self.page.locator("[data-test='tax-label']").inner_text()
        tax = float(tax_text.split('$')[1])
        expected_total = sum(prices) + tax

        total_price_text = self.page.locator("[data-test='total-label']").inner_text()
        total_price = float(total_price_text.split('$')[1])

        assert total_price == expected_total

        self.page.locator('[data-test="finish"]').click()

        expect(self.page.locator(".complete-header")).to_have_text("Thank you for your order!")


