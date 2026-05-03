Feature: Sample
  @no_cookie
  Scenario: 로그인
    When 아이디 입력
    When 비밀번호 입력
    When [로그인 하기] 버튼 클릭
    Then "최우영" 강사명 노출
    Then "서울테스트" 학원명 노출

  Scenario: 유튜브 수업 생성
    When [수업 생성] 버튼 클릭
    When [유튜브] 클릭
    Then [다음] 버튼 비활성화
    When "https://www.youtube.com/shorts/DeesHHZfkFM" 유튜브 링크 입력
    Then [다음] 버튼 활성화
    When [다음] 버튼 클릭
    When 유튜브 수업 생성 모달 안 [수업 생성] 버튼 클릭
    Then "🐳1초짜리 영상🐳" 영상 제목 노출
    Then 수업 생성 완료까지 대기
    Then 수업 초기화

  Scenario: 마켓에서 책 검색
    Given 마켓 페이지로 이동
    Then "2024년 10월 시행 고2 모의고사" 책이 노출
    When "[A*List] BEST Phonics 1" 책 검색
    When [검색] 버튼 클릭
    Then "[A*List] BEST Phonics 1" 책이 노출
