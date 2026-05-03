from pytest_bdd import scenario


@scenario('../features/sample.feature', '로그인')
def test_login():
    pass

@scenario('../features/sample.feature', '유튜브 수업 생성')
def test_create_youtube_class():
    pass

@scenario('../features/sample.feature', '마켓에서 책 검색')
def test_search_book_in_market():
    pass
