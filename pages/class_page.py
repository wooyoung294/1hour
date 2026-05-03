from common.base import Base


class ClassPage(Base):
    YOUTUBE_LINK_INPUT = '[placeholder="유튜브 링크를 입력해주세요."]'

    def click_youtube(self):
        self.page.locator('h3', has_text='유튜브').click()

    def fill_youtube_link(self, link: str):
        self.type(self.YOUTUBE_LINK_INPUT, link)

    def click_next_btn(self):
        self.page.get_by_role('button', name='다음', exact=True).click()

    def click_create_class_btn(self):
        self.page.get_by_role('button', name='수업 생성', exact=True).click()

    def click_create_class_btn_in_modal(self):
        modal = self.page.locator('[class*="modal_modal-container"]')
        modal.get_by_role('button', name='수업 생성', exact=True).click()

    def verify_next_btn_disabled(self):
        self.expect_disabled(self.page.get_by_role('button', name='다음', exact=True))

    def verify_next_btn_enabled(self):
        self.expect_enabled(self.page.get_by_role('button', name='다음', exact=True))
