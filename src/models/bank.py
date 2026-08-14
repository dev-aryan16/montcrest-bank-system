class Bank:
    def __init__(self, bank_id, bank_name):
        self.bank_id = bank_id
        self.bank_name = bank_name
        self.customers = []
        self.accounts = []
        self.transactions = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_account(self, account):
        self.accounts.append(account)

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None