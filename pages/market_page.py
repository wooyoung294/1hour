import os

from common.base import Base


class MarketPage(Base):
    SEARCH_INPUT = '[placeholder="책 제목을 입력해 주세요."]'

    def goto(self):
        self.page.goto(os.getenv('MARKET_URL'), wait_until='domcontentloaded')

    def fill_search(self, keyword: str):
        self.type(self.SEARCH_INPUT, keyword)

    def click_search_btn(self):
        self.page.get_by_role('button', name='검색', exact=True).click()

    def verify_book_title(self, title: str):
        self.expect_contain_text(self.page.locator('[class*="channel-list_channel-title"]').first, title)
