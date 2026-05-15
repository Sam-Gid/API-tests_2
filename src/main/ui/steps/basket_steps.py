import allure
from playwright.sync_api import Page
from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)
        self.back_to_catalog_button = page.locator("#continue-shopping")

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Проверяем наличие товара {product_name} в корзине")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)
        return self

    @allure.step("Проверяем отсутствие товара {product_name} в корзине")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)
        return self

    @allure.step("Получаем список товаров")
    def get_item_names(self):
        return self.basket.get_item_names()

    @allure.step("Получаем список цен товаров")
    def get_item_prices(self):
        return self.basket.get_item_prices()

    @allure.step("Получаем общую стоимость всех товаров в корзине")
    def get_items_in_cart_total_price(self):
        return self.basket.get_items_total_price()

    @allure.step("Удаляем товар {product_name} из корзины")
    def remove_from_cart(self, product_name: str):
        self.basket.remove_from_cart(product_name)
        self.expect_item_not_in_cart(product_name)
        return self