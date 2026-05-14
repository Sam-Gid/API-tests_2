from playwright.sync_api import expect
from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage
from src.main.ui.pages.login_page import LoginPage


def test_add_item_and_check_in_basket(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    button = catalog_page.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text('Remove')


def test_add_several_items_and_check_in_basket(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    catalog_page.add_to_cart("Sauce Labs Bike Light")
    catalog_page.add_to_cart("Sauce Labs Onesie")

    basket_page = BasketPage(page)

    basket_page.open_cart()
    basket_page.expect_item_in_cart("Sauce Labs Bike Light")
    basket_page.expect_item_in_cart("Sauce Labs Onesie")


def test_remove_item_from_basket(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    catalog_page.add_to_cart("Sauce Labs Bike Light")

    basket_page = BasketPage(page)

    basket_page.open_cart()
    basket_page.remove_from_cart("Sauce Labs Bike Light")
    basket_page.expect_item_not_in_cart("Sauce Labs Bike Light")


def test_remove_several_items_from_basket(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    catalog_page.add_to_cart("Sauce Labs Bike Light")
    catalog_page.add_to_cart("Sauce Labs Onesie")

    basket_page = BasketPage(page)

    basket_page.open_cart()
    basket_page.remove_from_cart("Sauce Labs Bike Light")
    basket_page.remove_from_cart("Sauce Labs Onesie")
    basket_page.expect_item_not_in_cart("Sauce Labs Bike Light")
    basket_page.expect_item_not_in_cart("Sauce Labs Onesie")


def test_checkout_several_items(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)

    catalog_page.add_to_cart("Sauce Labs Bike Light")
    catalog_page.add_to_cart("Sauce Labs Onesie")

    BasketPage(page).open_cart()

    checkout_page = CheckoutPage(page)

    checkout_page.open_checkout()
    checkout_page.fill_checkout_info("Sam", "Gid", "1212")
    checkout_page.start_checkout()


def test_checkout_without_items(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    CatalogPage(page).add_to_cart("Sauce Labs Bike Light")

    BasketPage(page).open_cart()

    checkout_page = CheckoutPage(page)

    checkout_page.open_checkout()
    page.get_by_placeholder("First Name").fill("Sam")
    page.get_by_placeholder("Last Name").fill("Gid")
    checkout_page.continue_button.click()
    error_message = checkout_page.error_message
    expect(error_message).to_have_text("Error: Postal Code is required")