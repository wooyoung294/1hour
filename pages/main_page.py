from common.base import Base


class MainPage(Base):
    def click_create_class_btn(self):
        self.page.get_by_role('link', name='수업 생성').click()
