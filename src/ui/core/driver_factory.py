from playwright.sync_api import sync_playwright
from config.settings import settings


class DriverFactory:

    def __init__(self):
        self.playwright = sync_playwright().start()

    def get_browser(self):
        browser_type = getattr(self.playwright, settings.browser)
        return browser_type.launch(headless=settings.headless)

    def create_page(self):
        browser = self.get_browser()
        context = browser.new_context()
        page = context.new_page()
        return page, browser