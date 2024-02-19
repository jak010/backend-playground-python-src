class BrokerageAccount:

    def __init__(self, account_number, customer, investments):
        self.account_number = account_number
        self.customer = customer
        self.investments = investments

    def get_customer(self):
        return self.customer

    def get_investments(self):
        return self.investments
