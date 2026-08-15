from src.models.account import BankAccount


class CurrentAccount(BankAccount):

    def __init__(
        self,
        account_number,
        customer,
        balance,
        status,
        created_at,
        overdraft_limit=50000
    ):
        super().__init__(
            account_number,
            customer,
            balance,
            "Current",
            status,
            created_at
        )
        self.overdraft_limit = overdraft_limit

    def calculate_interest(self):
        return 0