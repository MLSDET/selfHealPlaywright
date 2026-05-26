import os
from datetime import datetime


def take_screenshot(page, name="screenshot"):
    folder = "reports/screenshots"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{folder}/{name}_{timestamp}.png"

    page.screenshot(path=path)
    return path