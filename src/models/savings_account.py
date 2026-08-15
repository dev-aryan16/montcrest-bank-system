from src.models.account import BankAccount


class SavingsAccount(BankAccount):

    def __init__(
        self,
        account_number,
        customer,
        balance,
        status,
        created_at,
        interest_rate=0.04
    ):
        super().__init__(
            account_number,
            customer,
            balance,
            "Savings",
            status,
            created_at
        )
        self.interest_rate = interest_rate

    def calculate_interest(self):
        return self.balance * self.interest_rate