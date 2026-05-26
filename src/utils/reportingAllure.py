# src/utils/reporting.py
import allure
from functools import wraps


def report_step(step_name):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            with allure.step(step_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator