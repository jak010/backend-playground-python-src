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


def deposit2(to: str, amount: int):
    database.update_one(to, {'$inc': {'balance': amount}})


def transfer(from_account: str, to: str, amount: int):
    from_account_id = database.find(from_account)
    database.update_one(from_account_id, {'$inc': {'balance': -amount}})

    to_account_id = database.find(to)
    database.update_one(to_account_id, {'$inc': {'balance': amount}})
