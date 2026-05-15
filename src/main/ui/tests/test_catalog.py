from playwright.sync_api import expect
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_count_catalog(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    assert steps.get_products_count() == 6


def test_sorted_by_name(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    sorted_az = steps.sort_items("az").get_product_names()
    assert sorted_az == sorted(sorted_az)

    sorted_za = steps.sort_items("za").get_product_names()
    assert sorted_za == sorted(sorted_za, reverse=True)


def test_sort_by_price(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    sorted_lo_hi = steps.sort_items("lohi").get_product_prices()
    assert sorted_lo_hi == sorted(sorted_lo_hi)

    sorted_hi_lo = steps.sort_items("hilo").get_product_prices()
    assert sorted_hi_lo == sorted(sorted_hi_lo, reverse=True)


def test_add_to_cart(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    assert steps.get_cart_count() == 0

    steps.add_to_cart("Sauce Labs Bike Light")
    assert steps.get_cart_count() == 1


def test_add_sauce_labs_onesie_to_cart(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    assert steps.get_cart_count() == 0

    steps.add_to_cart("Sauce Labs Onesie").get_cart_count()
    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 0


def test_product_details_onesie(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price


def test_product_details_fleece_jacket(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_catalog(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    button = steps.remove_from_cart("Sauce Labs Onesie")
    expect(button).to_have_text("Add to cart")