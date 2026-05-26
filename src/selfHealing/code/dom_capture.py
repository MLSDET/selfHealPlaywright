from pathlib import Path

from playwright.sync_api import sync_playwright
import os
from src.ui.core.driver_factory import DriverFactory
from src.ui.pages.checkout_page import CheckoutPage
from src.ui.pages.inventory_page import InventoryPage
from src.ui.pages.login_page import LoginPage

CURRENT_DIR = Path(__file__).resolve().parent
HEALING_FOLDER = CURRENT_DIR.parent

class DOMCapture:

    def __init__(self):
        factory = DriverFactory()
        self.page, self.browser = factory.create_page()
        login = LoginPage(self.page)
        login.load()
        login.login()

    def capture_dom(self, pageName):

        match pageName:
            case "InventoryPage":
                self.capturingPage= self.page
            case "CheckOut":
                self.capturingPage = InventoryPage(self.page)
                self.capturingPage.go_to_cart()
                self.capturingPage = CheckoutPage(self.page)
            case _:
                print("no page name")

        dom=self.capturingPage.content()

        # # 1. Get the absolute path of the current script (dom_capture.py)
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        #
        # # 2. Go one levels up to reach the 'selfHealing' directory
        # self_healing_dir = os.path.abspath(os.path.join(script_dir, ".."))
        #
        # # 3. Target the 'pages_html' directory inside 'selfHealing'
        # output_dir = os.path.join(self_healing_dir, "pages_html")
        #
        # # 4. Create the 'pages_html' folder if it doesn't exist yet
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)
        #
        # # 5. Combine directory and filename
        # file_path = os.path.join(output_dir, f"{pageName}.html")
        htmlPath= HEALING_FOLDER / "pages_html" / f"{pageName}.html"

        # Ensure the 'models' directory exists before saving
        htmlPath.parent.mkdir(parents=True, exist_ok=True)
        # 6. Save the file safely
        with open(htmlPath, "w", encoding="utf-8") as file:
            file.write(dom)

        self.browser.close()



if __name__=="__main__":
    capture=DOMCapture()
    capture.capture_dom("InventoryPage")