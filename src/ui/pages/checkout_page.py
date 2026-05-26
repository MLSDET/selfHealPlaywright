from src.ui.core.base_page import BasePage
from src.utils.reportingAllure import report_step


class CheckoutPage(BasePage):

    CHECKOUT_BTN = "#checkout"
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    ZIP = "#postal-code"
    CONTINUE = "#continue"
    FINISH = "#finish"
    SUCCESS_MSG = ".complete-header"

    @report_step("Start checkout")
    def start_checkout(self):
        self.click(self.CHECKOUT_BTN)

    @report_step("Start checkout")
    def fill_details(self, first, last, zip_code):
        self.fill(self.FIRST_NAME, first)
        self.fill(self.LAST_NAME, last)
        self.fill(self.ZIP, zip_code)
        self.click(self.CONTINUE)

    @report_step("Finish Checkout")
    def finish_checkout(self):
        self.click(self.FINISH)

    @report_step("Get Success message")
    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)