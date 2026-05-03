import allure
from playwright.sync_api import Page
from pytest_bdd import parsers, then

from pages.lesson_page import LessonPage


@then(parsers.parse('"{title}" 영상 제목 노출'))
@allure.step('"{title}" 영상 제목 노출')
def verify_video_title(web_function_driver: Page, title: str):
    LessonPage(web_function_driver).verify_video_title(title)


@then('수업 생성 완료까지 대기')
@allure.step('수업 생성 완료까지 대기')
def wait_for_class_finished(data_store, web_function_driver: Page):
    LessonPage(web_function_driver).wait_for_class_finished(
        data_store.get('lesson_id'),
        data_store.get('auth_token'),
    )


@then('수업 초기화')
@allure.step('수업 초기화')
def clear_lesson(data_store, web_function_driver: Page):
    LessonPage(web_function_driver).delete_lesson(
        data_store.get('lesson_id'),
        data_store.get('auth_token'),
    )
