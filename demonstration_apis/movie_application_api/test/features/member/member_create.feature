Feature: 사용자 계정 만들기

  Scenario: 사용자는 계정을 만들 수 있습니다.
    Given 사용자는 name 을 입력합니다.
    When 입력된 name과 함께 사용자 entity를 생성합니다.
    Then 생성된 entity는 24자리의 고유 id를 가집니다.