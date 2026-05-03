import allure
from playwright.sync_api import Page
from pytest_bdd import when

from pages.main_page import MainPage


@when('[수업 생성] 버튼 클릭')
@allure.step('[수업 생성] 버튼 클릭')
def click_create_class_btn(web_function_driver: Page):
    MainPage(web_function_driver).click_create_class_btn()
