import allure
from playwright.sync_api import Page
from pytest_bdd import when

from pages.login_page import LoginPage


@when('아이디 입력')
@allure.step('아이디 입력')
def fill_id(web_function_driver: Page):
    LoginPage(web_function_driver).fill_id_from_env()


@when('비밀번호 입력')
@allure.step('비밀번호 입력')
def fill_password(web_function_driver: Page):
    LoginPage(web_function_driver).fill_password_from_env()


@when('[로그인 하기] 버튼 클릭')
@allure.step('[로그인 하기] 버튼 클릭')
def click_login_btn(web_function_driver: Page):
    LoginPage(web_function_driver).click_login_btn()
