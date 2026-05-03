"""액션 베이스 - 클릭, 입력 등 페이지 조작."""

from typing import TYPE_CHECKING, Callable

from playwright.sync_api import Locator

from common.decorators import log_on_failure

if TYPE_CHECKING:
    from playwright.sync_api import Page


class ActionBase:
    page: 'Page'
    expect_visible: Callable

    @log_on_failure
    def click(self, target: str | Locator, **kwargs):
        if isinstance(target, Locator):
            target.click()
        else:
            self.page.locator(target, **kwargs).click()

    @log_on_failure
    def click_by_text(self, text: str, exact: bool = False) -> None:
        self.page.get_by_text(text, exact=exact).click()

    @log_on_failure
    def scroll_and_click(self, selector: str, **kwargs) -> None:
        element = self.page.locator(selector, **kwargs)
        element.scroll_into_view_if_needed()
        self.expect_visible(selector)
        element.click()

    @log_on_failure
    def type(self, target: str | Locator, text: str, **kwargs) -> None:
        if isinstance(target, Locator):
            target.type(text)
        else:
            self.page.locator(target, **kwargs).type(text)

    @log_on_failure
    def fill(self, target: str | Locator, text: str, **kwargs) -> None:
        if isinstance(target, Locator):
            target.fill(text)
        else:
            self.page.locator(target, **kwargs).fill(text)

    @log_on_failure
    def stable_click(self, target: str, stable_target: str) -> None:
        self.click(target)
        self.expect_visible(stable_target)
