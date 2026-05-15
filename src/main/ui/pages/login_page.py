from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils.constansts import Urls


class LoginPage(BasePage):
    URL = Urls.BASE

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()
