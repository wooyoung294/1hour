import os

from common.base import Base


class LoginPage(Base):
    ID_INPUT = '[placeholder="아이디를 입력하세요"]'
    PASSWORD_INPUT = '[placeholder="비밀번호를 입력하세요"]'

    def fill_id_from_env(self):
        self.type(self.ID_INPUT, os.getenv('1HOUR_ID'))

    def fill_password_from_env(self):
        self.type(self.PASSWORD_INPUT, os.getenv('1HOUR_PASS'))

    def click_login_btn(self):
        self.page.get_by_text('로그인 하기', exact=True).click()
