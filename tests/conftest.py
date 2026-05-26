import allure
import pytest
import os
import pytest_html
from src.ui.core.driver_factory import DriverFactory
from src.utils.report_utils import take_screenshot


def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)


@pytest.fixture
def page():
    factory = DriverFactory()
    page, browser = factory.create_page()
    yield page
    browser.close()


# 🔥 Attach screenshots on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            screenshot_path = take_screenshot(page, item.name)

            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            if hasattr(report, "extra"):
                report.extra.append(
                    pytest_html.extras.image(screenshot_path)

                )
def pytest_html_report_title(report):
    report.title = "TestGuardian AI - Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        "<h2>Self-Healing Test Automation Report</h2>"
    ])


def pytest_html_results_table_header(cells):
    cells.insert(1, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(1, f"<td>{report.nodeid}</td>")