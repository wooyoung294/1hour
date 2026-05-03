import allure
from playwright.sync_api import Page
from pytest_bdd import parsers, then, when

from pages.class_page import ClassPage


@when('[유튜브] 클릭')
@allure.step('[유튜브] 클릭')
def click_youtube(web_function_driver: Page):
    ClassPage(web_function_driver).click_youtube()


@when(parsers.parse('"{link}" 유튜브 링크 입력'))
@allure.step('"{link}" 유튜브 링크 입력')
def fill_youtube_link(web_function_driver: Page, link: str):
    ClassPage(web_function_driver).fill_youtube_link(link)


@when('[다음] 버튼 클릭')
@allure.step('[다음] 버튼 클릭')
def click_next_btn(web_function_driver: Page):
    ClassPage(web_function_driver).click_next_btn()


@when('유튜브 수업 생성 모달 안 [수업 생성] 버튼 클릭')
@allure.step('유튜브 수업 생성 모달 안 [수업 생성] 버튼 클릭')
def click_create_class_btn_in_modal(web_function_driver: Page):
    ClassPage(web_function_driver).click_create_class_btn_in_modal()


@then('[다음] 버튼 비활성화')
@allure.step('[다음] 버튼 비활성화')
def verify_next_btn_disabled(web_function_driver: Page):
    ClassPage(web_function_driver).verify_next_btn_disabled()


@then('[다음] 버튼 활성화')
@allure.step('[다음] 버튼 활성화')
def verify_next_btn_enabled(web_function_driver: Page):
    ClassPage(web_function_driver).verify_next_btn_enabled()
