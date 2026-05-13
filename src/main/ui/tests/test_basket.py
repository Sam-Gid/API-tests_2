from playwright.sync_api import expect
from src.main.ui.pages.basket_page import BasketPage


def test_add_item_and_check_in_cart(page):
    page = BasketPage(page)
    page.login("standard_user", "secret_sauce")

    button = page.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    assert page.get_cart_count() == 1


def test_add_several_items_and_check_in_cart(page):
    page = BasketPage(page)
    page.login("standard_user", "secret_sauce")

    button_1 = page.add_to_cart("Sauce Labs Bike Light")
    expect(button_1).to_have_text("Remove")
    assert page.get_cart_count() == 1

    button_2 = page.add_to_cart("Sauce Labs Onesie")
    expect(button_2).to_have_text("Remove")
    assert page.get_cart_count() == 2


def test_remove_item_from_cart(page):
    page = BasketPage(page)
    page.login("standard_user", "secret_sauce")

    page.add_to_cart("Sauce Labs Bike Light")
    assert page.get_cart_count() == 1

    remove_button = page.remove_from_cart("Sauce Labs Bike Light")
    expect(remove_button).to_have_text("Add to cart")


def test_remove_several_items_from_cart(page):
    page = BasketPage(page)
    page.login("standard_user", "secret_sauce")

    page.add_to_cart("Sauce Labs Bike Light")
    page.add_to_cart("Sauce Labs Onesie")
    assert page.get_cart_count() == 2

    remove_button_1 = page.remove_from_cart("Sauce Labs Bike Light")
    remove_button_2 = page.remove_from_cart("Sauce Labs Onesie")
    expect(remove_button_1).to_have_text("Add to cart")
    expect(remove_button_2).to_have_text("Add to cart")

def test_checkout_several_items(page):
    page = BasketPage(page)
    page.login("standard_user", "secret_sauce")

    page.add_to_cart("Sauce Labs Bike Light")
    page.add_to_cart("Sauce Labs Onesie")
    assert page.get_cart_count() == 2

    page.open_cart()
    page.checkout_button.click()

    page.fill_checkout_info("Sam", "Gid", "1212")
    page.checkout_info()


def test_checkout_without_items(auth_page):
    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()

    auth_page.locator(".shopping_cart_link").click()

    jacket = auth_page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    assert jacket.is_visible()

    auth_page.locator('[data-test="checkout"]').click()

    auth_page.get_by_placeholder("First Name").fill("Sam")
    auth_page.get_by_placeholder("Last Name").fill("Gid")

    auth_page.locator('[data-test="continue"]').click()

    error_message = auth_page.locator('[data-test="error"]')
    expect(error_message).to_have_text("Error: Postal Code is required")