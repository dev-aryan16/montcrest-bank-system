from src.models.account import BankAccount


class FixedDepositAccount(BankAccount):

    def __init__(
        self,
        account_number,
        customer,
        balance,
        status,
        created_at,
        interest_rate=0.07,
        tenure_years=1
    ):
        super().__init__(
            account_number,
            customer,
            balance,
            "Fixed Deposit",
            status,
            created_at
        )
        self.interest_rate = interest_rate
        self.tenure_years = tenure_years

    def calculate_interest(self):
        return self.balance * self.interest_rate * self.tenure_years