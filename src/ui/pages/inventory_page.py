from src.selfHealing.runtime.self_heal_engine import SelfHealingEngine
from src.ui.core.base_page import BasePage
from src.utils.reportingAllure import report_step


class InventoryPage(BasePage):

    ADD_TO_CART_BTN = "#add-to-cart-sauce-labs-back"
    CART_ICON = ".shopping_cart_link"
    healer = SelfHealingEngine()

    @report_step("Add items to cart")
    def add_item_to_cart(self):
        self.healer.safe_click(self.page,self.ADD_TO_CART_BTN)

    @report_step("Go to cart")
    def go_to_cart(self):
        self.click(self.CART_ICON)