from poetry.console.commands import self

from src.ui.pages.login_page import LoginPage
from src.ui.pages.inventory_page import InventoryPage
from src.ui.pages.checkout_page import CheckoutPage
from playwright.sync_api import expect


def test_checkout(page):
    login = LoginPage(page)
    login.load()
    login.login()

    inventory = InventoryPage(page)
    inventory.add_item_to_cart()
    inventory.go_to_cart()

    checkout = CheckoutPage(page)
    checkout.start_checkout()
    checkout.fill_details("Ramya", "Shetty", "560001")
    checkout.finish_checkout()

    assert "Thank you" in checkout.get_success_message()