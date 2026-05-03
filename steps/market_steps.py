import time

import allure
from playwright.sync_api import Page
from pytest_bdd import given, parsers, then, when

from pages.market_page import MarketPage


@given('마켓 페이지로 이동')
@allure.step('마켓 페이지로 이동')
def goto_market(web_function_driver: Page):
    MarketPage(web_function_driver).goto()


@when(parsers.parse('"{keyword}" 책 검색'))
@allure.step('"{keyword}" 책 검색')
def fill_search(web_function_driver: Page, keyword: str):
    MarketPage(web_function_driver).fill_search(keyword)


@when('[검색] 버튼 클릭')
@allure.step('[검색] 버튼 클릭')
def click_search_btn(web_function_driver: Page):
    MarketPage(web_function_driver).click_search_btn()

@then(parsers.parse('"{title}" 책이 노출'))
@allure.step('"{title}" 책이 노출')
def verify_book_title(web_function_driver: Page, title: str):
    MarketPage(web_function_driver).verify_book_title(title)
