"""공통 유틸리티."""

from playwright.sync_api import Locator


def get_next_element(target: Locator, step: int = 1) -> Locator:
    """해당 요소의 다음 형제 요소를 가져온다."""
    return target.locator(f'xpath=following-sibling::*[{step}]')


def get_prev_element(target: Locator, step: int = 1) -> Locator:
    """해당 요소의 이전 형제 요소를 가져온다."""
    return target.locator(f'xpath=preceding-sibling::*[{step}]')
