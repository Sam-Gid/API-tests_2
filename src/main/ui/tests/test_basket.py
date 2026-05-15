from playwright.sync_api import expect
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_add_item_and_check_in_basket(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")


def test_add_several_items_and_check_in_cart(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    catalog.add_to_cart("Sauce Labs Onesie")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")
    basket.expect_item_in_cart("Sauce Labs Onesie")


def test_remove_item_from_basket(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")
    basket.remove_from_cart("Sauce Labs Bike Light")
    basket.expect_item_not_in_cart("Sauce Labs Onesie")


def test_remove_several_items_from_basket(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    catalog.add_to_cart("Sauce Labs Onesie")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")
    basket.expect_item_in_cart("Sauce Labs Onesie")
    basket.remove_from_cart("Sauce Labs Bike Light")
    basket.remove_from_cart("Sauce Labs Onesie")
    basket.expect_item_not_in_cart("Sauce Labs Bike Light")
    basket.expect_item_not_in_cart("Sauce Labs Onesie")


def test_checkout_several_items(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    catalog.add_to_cart("Sauce Labs Onesie")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")
    basket.expect_item_in_cart("Sauce Labs Onesie")
    checkout = CheckoutSteps(page)
    basket_total = basket.get_items_in_cart_total_price()
    checkout.open_checkout_page().fill_checkout_info("Sam", "Gid", "1212")
    checkout_total = checkout.get_item_total_price_after_continue()
    assert basket_total == checkout_total, "Сумма товаров в Checkout не совпадает с суммой товаров в корзине"
    checkout.finish_checkout()
    success_text = checkout.get_success_text()
    assert success_text == "Thank you for your order!", "Покупка не завершена или завершена с ошибкой"


def test_checkout_without_items(page):
    login_page = LoginSteps(page)
    login_page.open_login_page().login("standard_user", "secret_sauce")
    catalog = CatalogSteps(page)
    catalog.add_to_cart("Sauce Labs Bike Light")
    catalog.add_to_cart("Sauce Labs Onesie")
    basket = BasketSteps(page)
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Bike Light")
    basket.expect_item_in_cart("Sauce Labs Onesie")
    checkout = CheckoutSteps(page)
    checkout.open_checkout_page().fill_checkout_info("Sam", "Gid", "")
    error_message = checkout.error_message
    (expect(error_message).to_have_text("Error: Postal Code is required"),
     "Ошибка: отправленные данные не должны быть приняты")