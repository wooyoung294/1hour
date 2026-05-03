from common.base import Base


class Header(Base):
    @property
    def root(self):
        return self.page.locator('header')

    def verify_instructor_name(self, name: str):
        self.expect_contain_text(self.root, name)

    def verify_academy_name(self, name: str):
        self.expect_contain_text(self.root, name)
