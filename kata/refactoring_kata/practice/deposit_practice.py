"""

한 계좌에서 돈을 인출해서 다른 계좌에 입금하는 은행 거래를 두 부분으로 분할,
이는 실수로 deposit 메서드를 잘못 호출하면 출금없이 돈을 입금할 수도 있음을 의미한다.
이 상황을 해결하기 위해 두 가지 메서드를 결합하자.

# 절차
1. 메서드의 이름을 임시로 변경합니다. 그러면 함수를 사용하는 모든 곳에서 컴파일 오류가 발생합니다.
2. 메서드의 본문을 복사하고 매개변수를 기억해둡니다.
3. 컴파일러가 오류를 발생시킨 모든 곳의 호출을 복사된 코드로 교체하고 인자를 매개변수에 매핑합니다.
4. 오류 없이 컴파일되면 원래의 메서드가 더 이상 사용되지 않는 것이므로 원래 메서드를 삭제합니다.
"""


class Database:
    def __init__(self):
        self.accounts = {}

    def find(self, account_name: str):
        return self.accounts.get(account_name, {'balance': 0})

    def update_one(self, account_name: str, update: dict):
        if account_name not in self.accounts:
            self.accounts[account_name] = {'balance': 0}
        self.accounts[account_name]['balance'] += update.get('$inc', {}).get('balance', 0)


database = Database()


def deposit(to: str, amount: int):
    account_id = database.find(to)
    database.update_one(to, {'$inc': {'balance': amount}})


def transfer(from_account: str, to: str, amount: int):
    deposit(from_account, -amount)
    deposit(to, amount)
