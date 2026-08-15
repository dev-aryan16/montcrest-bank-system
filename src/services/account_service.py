from src.models.savings_account import SavingsAccount
from src.models.current_account import CurrentAccount
from src.models.fixed_deposit import FixedDepositAccount


class AccountService:

    def __init__(self, account_repository):
        self.account_repository = account_repository

    def _generate_account_number(self):
        accounts = self.account_repository.get_all()

        if not accounts:
            return 1000001

        highest_number = max(
            account.account_number
            for account in accounts
        )

        return highest_number + 1

    def create_account(
        self,
        customer_id,
        customer,
        account_type,
        initial_balance,
        status="ACTIVE",
        created_at=None
    ):
        account_number = self._generate_account_number()

        account_type = account_type.upper()

        if account_type == "SAVINGS":
            account = SavingsAccount(
                account_number=account_number,
                customer=customer,
                balance=initial_balance,
                status=status,
                created_at=created_at
            )

        elif account_type == "CURRENT":
            account = CurrentAccount(
                account_number=account_number,
                customer=customer,
                balance=initial_balance,
                status=status,
                created_at=created_at
            )

        elif account_type == "FIXED_DEPOSIT":
            account = FixedDepositAccount(
                account_number=account_number,
                customer=customer,
                balance=initial_balance,
                status=status,
                created_at=created_at
            )

        else:
            raise ValueError(
                f"Unsupported account type: {account_type}"
            )

        account_data = {
            "account_number": account.account_number,
            "customer_id": customer_id,
            "balance": account.balance,
            "account_type": account.account_type,
            "status": account.status
        }

        return self.account_repository.create(account_data)

    def get_account(self, account_number):
        account = self.account_repository.get_by_account_number(
            account_number
        )

        if account is None:
            raise ValueError(
                f"Account {account_number} not found."
            )

        return account

    def get_customer_accounts(self, customer_id):
        return self.account_repository.get_by_customer_id(
            customer_id
        )

    def get_all_accounts(self):
        return self.account_repository.get_all()

    def update_account(self, account_number, updates):
        account = self.get_account(account_number)

        for field, value in updates.items():
            if hasattr(account, field):
                setattr(account, field, value)

        return self.account_repository.update(account)

    def delete_account(self, account_number):
        account = self.get_account(account_number)

        deleted = self.account_repository.delete(
            account.account_number
        )

        if not deleted:
            raise ValueError(
                f"Unable to delete account {account_number}."
            )

        return True