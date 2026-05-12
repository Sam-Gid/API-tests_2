from playwright.sync_api import expect


def test_add_item_and_check_in_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    page.locator(".shopping_cart_link").click()

    item_name = page.locator('[data-test="inventory-item-name"]')
    assert item_name.inner_text() == "Sauce Labs Backpack"


def test_add_several_items_and_check_in_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()

    page.locator(".shopping_cart_link").click()

    item_one_name = page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    assert item_one_name.is_visible()

    item_two_name = page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Bolt T-Shirt")
    assert item_two_name.is_visible()


def test_remove_item_from_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    page.locator(".shopping_cart_link").click()

    jacket = page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')
    expect(jacket).to_be_visible()

    page.locator('[data-test="remove-sauce-labs-fleece-jacket"]').click()

    expect(jacket).not_to_be_visible()


def test_remove_several_items_from_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()
    page.locator(".shopping_cart_link").click()

    item_one = page.locator('.inventory_item_name', has_text='Sauce Labs Backpack')
    expect(item_one).to_be_visible()

    item_two = page.locator('.inventory_item_name', has_text='Test.allTheThings() T-Shirt (Red)')
    expect(item_two).to_be_visible()

    page.locator('[data-test="remove-sauce-labs-backpack"]').click()
    page.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]').click()

    expect(item_one).not_to_be_visible()
    expect(item_two).not_to_be_visible()


def test_checkout_several_items(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()

    page.locator(".shopping_cart_link").click()

    item_one_name = page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    assert item_one_name.is_visible()

    item_two_name = page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Bolt T-Shirt")
    assert item_two_name.is_visible()

    page.locator('[data-test="checkout"]').click()

    page.get_by_placeholder("First Name").fill("Sam")
    page.get_by_placeholder("Last Name").fill("Gid")
    page.get_by_placeholder("Zip/Postal Code").fill("1212")

    page.locator('[data-test="continue"]').click()

    prices_text = page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_text]
    tax_text = page.locator("[data-test='tax-label']").inner_text()
    tax = float(tax_text.split('$')[1])
    expected_total = sum(prices) + tax

    total_price_text = page.locator("[data-test='total-label']").inner_text()
    total_price = float(total_price_text.split('$')[1])

    assert total_price == expected_total

    page.locator('[data-test="finish"]').click()

    expect(
        page.locator(".complete-header")).to_have_text("Thank you for your order!")


def test_checkout_without_items(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()

    page.locator(".shopping_cart_link").click()

    jacket = page.locator('[data-test="inventory-item-name"]', has_text="Sauce Labs Fleece Jacket")
    assert jacket.is_visible()

    page.locator('[data-test="checkout"]').click()

    page.get_by_placeholder("First Name").fill("Sam")
    page.get_by_placeholder("Last Name").fill("Gid")

    page.locator('[data-test="continue"]').click()

    error_message = page.locator('[data-test="error"]')
    expect(error_message).to_have_text("Error: Postal Code is required")