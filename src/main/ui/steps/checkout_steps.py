import allure
from playwright.sync_api import Page
from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)
        self.error_message = page.locator('[data-test="error"]')

    @allure.step("Открываем страницу оформления покупки")
    def open_checkout_page(self):
        self.checkout.open_checkout()
        return self

    @allure.step("Заполняем поля на странице оформления покупки")
    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        self.checkout.fill_checkout_info(first_name, last_name, zip_code)
        return self

    @allure.step("Получаем текст об успешном оформлении покупки")
    def get_success_text(self):
        return self.checkout.get_success_text()

    @allure.step("Получаем итоговую стоимость товаров ПОСЛЕ оформления покупки")
    def get_item_total_price_after_continue(self):
        return self.checkout.get_item_total_price_after_checkout()

    @allure.step("Проверяем оформление покупки")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self