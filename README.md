# 원아워

원아워(1hour.ai) 웹 E2E 자동화 테스트 (Playwright + pytest-bdd)

## 테스트 시나리오

| # | 시나리오 | 설명 |
|---|---------|------|
| 1 | 로그인 | 아이디/비밀번호 입력 → [로그인 하기] 클릭 |
| 2 | 유튜브 수업 생성 | 메인에서 [수업 생성] → [유튜브] → 링크 입력 → [다음] → 모달 [수업 생성] → `content_state` API 폴링으로 처리 완료 대기 → 영상 제목 검증 → API로 자동 삭제 |
| 3 | 마켓 책 검색 | 마켓 페이지로 직접 이동(Critical Path) → 책 제목 입력 → [검색] → 검색 결과 책 노출 검증 |

## 설계

### BDD + POM
| 패턴 | 설명 | 장점 |
|-----|------|------|
| **BDD** (pytest-bdd) | 한국어 Gherkin 시나리오로 작성 | 비개발자도 읽고 검토 가능 |
| **POM** (Page Object Model) | 페이지/컴포넌트 단위 클래스로 셀렉터·동작 캡슐화 | UI 변경 시 한 곳만 수정, 코드 재사용 |

흐름: `Feature → Step → Page Object`

### Critical Path 방식
- **URL 직접 이동**: 메인 → 카테고리 → 상세 같은 무의미한 클릭 체인 제거
- **API로 데이터 정리**: 테스트 후 cleanup을 UI가 아닌 API로 수행
- 결과: **테스트 시간 단축**, 불필요한 의존성 제거, 실패 원인 명확

### 세션 로그인 + 쿠키 재사용
- `web_session_driver`(session scope)에서 **딱 1번만 로그인** → `cookie_{worker_id}.json` 저장
- 이후 모든 테스트는 저장된 쿠키로 시작 → 매번 로그인 안 함
- 비회원 테스트는 `@no_cookie` 마커로 차단

### 실제 Google Chrome 사용
사이트의 차단을 피하기 위해 Playwright 번들 Chromium이 아닌 시스템 설치된 Chrome 사용
```python
playwright.chromium.launch(channel='chrome')
```

### 실패 시 자동 재시도
```ini
addopts = --reruns 1 --reruns-delay 2
```
네트워크 불안정·타이밍 이슈 같은 일시적 실패를 한번 더 돌려 flaky 케이스를 줄임.

---

## 이렇게 만들었어요

### 1. listener로 응답 ID · JWT 자동 수집

```python
def capture_lesson_response(response):
    if 'api-v1-b.1hour.ai/video/video/' in response.url and response.request.method == 'POST':
        data = response.json()
        if data.get('id'):
            data_store['lesson_id'] = data['id']

def capture_auth_token(req):
    if 'api-v1-b.1hour.ai' in req.url:
        auth = req.headers.get('authorization')
        if auth:
            data_store['auth_token'] = auth
```

### 2. data_store에서 데이터 관리

```python
@pytest.fixture
def data_store():
    return {}
```

### 3. 비동기 처리, sleep 대신 PATCH API 폴링

```python
def wait_for_class_finished(self, lesson_id, auth_token, timeout=120, interval=2):
    while time.time() < deadline:
        response = self.page.context.request.patch(url, headers=headers)
        if response.json().get('data', {}).get('status', {}).get('code') == 'FINISHED':
            return
        time.sleep(interval)
    raise TimeoutError(...)
```

### 4. 반복적인 테스트를 위해 테스트 후 cleanup

```gherkin
Then 수업 생성 완료까지 대기
Then "🐳1초짜리 영상🐳" 영상 제목 노출
Then 수업 초기화
```

### 5. parser로 검증 스텝 재사용

```python
@then(parsers.parse('"{title}" 영상 제목 노출'))
def verify_video_title(web_function_driver, title):
    LessonPage(web_function_driver).verify_video_title(title)
```
```gherkin
Then "🐳1초짜리 영상🐳" 영상 제목 노출
Then "[A*List] BEST Phonics 1" 책이 노출
```

### 6. component와 page 분리

```python
class Header(Base):
    @property
    def root(self):
        return self.page.locator('header')

    def verify_instructor_name(self, name):
        self.expect_contain_text(self.root, name)
```

---

## 구조

```
qaplat/
├── conftest.py             # fixture, listener, hook
├── pytest.ini              # 마커, addopts
├── .env                    # 환경변수
├── common/                 # Base, Action/Expect base, decorator
├── components/
│   └── header.py           # 헤더 컴포넌트 (root 스코핑)
├── configs/vars.qa.yaml    # 환경별 데이터
├── features/sample.feature # Gherkin 시나리오
├── pages/                  # Page Object
│   ├── login_page.py
│   ├── main_page.py
│   ├── class_page.py       # 수업 생성
│   ├── lesson_page.py      # 폴링·삭제 API
│   └── market_page.py      # 마켓 검색
├── steps/                  # 한국어 step
└── case/test_sample.py     # @scenario 엔트리
```

## 환경 변수

`.env`
```env
PAGE_URL=https://1hour.ai/kr/login
MARKET_URL=https://1hour.ai/kr/market/list
1HOUR_ID=your_id
1HOUR_PASS=your_password
```

## 요구 환경

- **Python**: 3.11 이상

## 사용 라이브러리

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| `playwright` | 1.54.0 | 브라우저 자동화 |
| `pytest` | 8.4.1 | 테스트 러너 |
| `pytest-bdd` | 8.1.0 | Gherkin 기반 BDD 시나리오 |
| `pytest-xdist` | 3.8.0 | 테스트 병렬 실행 |
| `pytest-rerunfailures` | 16.0.1 | 실패 시 자동 재시도 |
| `allure-pytest` | 2.15.0 | Allure 리포트 생성·첨부 |
| `loguru` | 0.7.3 | 로그 출력 |
| `python-dotenv` | 1.2.1 | `.env` 파일 로드 |
| `PyYAML` | 6.0.3 | 환경별 데이터(`vars.qa.yaml`) 파싱 |
| `tenacity` | 9.1.2 | 재시도 유틸 |
| `Pillow` | 12.1.0 | 이미지 처리(스크린샷) |

## 실행

```bash
pytest
```
