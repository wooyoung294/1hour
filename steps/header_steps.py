import allure
from playwright.sync_api import Page
from pytest_bdd import parsers, then

from components.header import Header


@then(parsers.parse('"{name}" 강사명 노출'))
@allure.step('"{name}" 강사명 노출')
def verify_instructor_name(web_function_driver: Page, name: str):
    Header(web_function_driver).verify_instructor_name(name)


@then(parsers.parse('"{name}" 학원명 노출'))
@allure.step('"{name}" 학원명 노출')
def verify_academy_name(web_function_driver: Page, name: str):
    Header(web_function_driver).verify_academy_name(name)

