from utils.exceptions import (
    InvalidAmountError,
    InsufficientBalanceError,
    AccountInactiveError
)


class BankAccount:

    def __init__(
        self,
        account_number,
        customer,
        balance,
        account_type,
        status,
        created_at
    ):
        self.account_number = account_number
        self.customer = customer
        self.__balance = balance
        self.account_type = account_type
        self.status = status
        self.created_at = created_at

    def deposit(self, amount):

        # Check account status
        if self.status != "ACTIVE":
            raise AccountInactiveError(
                "Cannot deposit into an inactive account."
            )

        # Check amount
        if amount <= 0:
            raise InvalidAmountError(
                "Deposit amount must be positive."
            )

        self.__balance += amount
        return True

    def withdraw(self, amount):

        # Check account status
        if self.status != "ACTIVE":
            raise AccountInactiveError(
                "Cannot withdraw from an inactive account."
            )

        # Check amount
        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be positive."
            )

        # Check available balance
        if amount > self.__balance:
            raise InsufficientBalanceError(
                "Insufficient funds."
            )

        self.__balance -= amount
        return True

    @property
    def balance(self):
        return self.__balance

    def get_balance(self):
        return self.__balance

    def get_account_info(self):
        return {
            "account_number": self.account_number,
            "customer": self.customer.get_full_name(),
            "balance": self.__balance,
            "account_type": self.account_type,
            "status": self.status,
            "created_at": self.created_at
        }





                