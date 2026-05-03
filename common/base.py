"""Base - 모든 페이지 객체와 컴포넌트의 기본 클래스."""

from playwright.sync_api import Page

from common.action_base import ActionBase
from common.expect_base import ExpectBase
from common.log_config import setup_logger
from common.log_mixin import LogMixin

setup_logger()


class Base(ActionBase, ExpectBase, LogMixin):
    def __init__(self, page: Page):
        self.page = page

    def get_context_info(self) -> str:
        return self.page.url
