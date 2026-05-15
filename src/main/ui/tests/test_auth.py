from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_auth(page):
    login = LoginSteps(page)
    login.open_login_page().login("standard_user", "secret_sauce")
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары не странице каталога"


def test_login_locked_out_user(page):
    login = LoginSteps(page)
    login.open_login_page().login("locked_out_user", "secret_sauce")
    error_text = login.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    assert steps.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    steps.logout()
    expect(page).to_have_url(LoginPage.URL), "Ожидаем возврат на страницу логина"


def test_visual_user_logout(page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    steps = CatalogSteps(page)
    assert steps.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    steps.logout()
    expect(page).to_have_url(LoginPage.URL), "Ожидаем возврат на страницу логина"

