from loguru import logger
import os

os.makedirs("reports/logs", exist_ok=True)

logger.add(
    "reports/logs/test.log",
    rotation="1 MB",
    level="INFO",
    format="{time} | {level} | {message}"
)