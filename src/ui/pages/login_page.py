from src.ui.core.base_page import BasePage
from config.settings import settings
from src.utils.reportingAllure import report_step


class LoginPage(BasePage):

    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"

    @report_step("Open login page")
    def load(self):
        self.page.goto(settings.base_url)

    @report_step("Login as standard user")
    def login(self):
        self.fill(self.USERNAME, settings.username)
        self.fill(self.PASSWORD, settings.password)
        self.click(self.LOGIN_BTN)