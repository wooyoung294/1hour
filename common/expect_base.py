"""검증 베이스 - 요소 상태 검증."""

from typing import TYPE_CHECKING

from playwright.sync_api import Locator, expect

from common.decorators import log_on_failure

if TYPE_CHECKING:
    from playwright.sync_api import Page


class ExpectBase:
    page: 'Page'

    @log_on_failure
    def expect_visible(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_be_visible(timeout=timeout)
        else:
            expect(self.page.locator(target)).to_be_visible(timeout=timeout)

    @log_on_failure
    def expect_text_visible(self, text: str, timeout: int = 10000, exact: bool = False) -> None:
        expect(self.page.get_by_text(text, exact=exact)).to_be_visible(timeout=timeout)

    @log_on_failure
    def expect_text(self, target: str | Locator, text: str, timeout: int = 10000, **kwargs) -> None:
        if isinstance(target, Locator):
            expect(target).to_have_text(text)
        else:
            expect(self.page.locator(target, **kwargs)).to_have_text(text, timeout=timeout)

    @log_on_failure
    def expect_contain_text(self, target: str | Locator, text: str, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_contain_text(text, timeout=timeout)
        else:
            expect(self.page.locator(target)).to_contain_text(text, timeout=timeout)

    @log_on_failure
    def expect_text_not_visible(self, text: str, timeout: int = 5000) -> None:
        expect(self.page.get_by_text(text)).not_to_be_visible(timeout=timeout)

    def expect_text_in_viewport(self, text: str, exact: bool = False) -> None:
        expect(self.page.get_by_text(text, exact=exact)).to_be_in_viewport()

    @log_on_failure
    def expect_disabled(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_be_disabled(timeout=timeout)
        else:
            expect(self.page.locator(target)).to_be_disabled(timeout=timeout)

    @log_on_failure
    def expect_not_disabled(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).not_to_be_disabled(timeout=timeout)
        else:
            expect(self.page.locator(target)).not_to_be_disabled(timeout=timeout)

    @log_on_failure
    def expect_enabled(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_be_enabled(timeout=timeout)
        else:
            expect(self.page.locator(target)).to_be_enabled(timeout=timeout)

    @log_on_failure
    def expect_value(self, target: str | Locator, value: str, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_have_value(value, timeout=timeout)
        else:
            expect(self.page.locator(target)).to_have_value(value, timeout=timeout)

    @log_on_failure
    def expect_not_visible(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).not_to_be_visible(timeout=timeout)
        else:
            expect(self.page.locator(target)).not_to_be_visible(timeout=timeout)

    @log_on_failure
    def expect_checked(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_be_checked(timeout=timeout)
        else:
            expect(self.page.locator(target)).to_be_checked(timeout=timeout)

    @log_on_failure
    def expect_unchecked(self, target: str | Locator, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).not_to_be_checked(timeout=timeout)
        else:
            expect(self.page.locator(target)).not_to_be_checked(timeout=timeout)

    @log_on_failure
    def expect_attribute(self, target: str | Locator, name: str, value: str, timeout: int = 5000) -> None:
        if isinstance(target, Locator):
            expect(target).to_have_attribute(name, value, timeout=timeout)
        else:
            expect(self.page.locator(target)).to_have_attribute(name, value, timeout=timeout)
