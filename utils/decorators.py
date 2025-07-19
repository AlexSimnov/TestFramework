import functools
import allure


def allure_test_details(
        story: str,
        title: str,
        description: str,
        severity: str,
        label: tuple):

    def decorator(func):
        @allure.story(story)
        @allure.title(title)
        @allure.description(description)
        @allure.severity(severity)
        @allure.label(label)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
