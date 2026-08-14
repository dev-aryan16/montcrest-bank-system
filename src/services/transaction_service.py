from models.transaction import Transaction
from models.bank import Bank


class TransactionService:

    def __init__(self, bank):
        self.bank = bank

    def process_deposit(self, account, amount):

        success = account.deposit(amount)

        if not success:
            return False

        transaction = Transaction(
            transaction_id=1,
            transaction_type="DEPOSIT",
            amount=amount,
            source_account=None,
            destination_account=account.account_number,
            timestamp="2026-08-15 10:00:00",
            status="COMPLETED"
        )

        self.bank.add_transaction(transaction)

        return True

    def process_withdrawal(self, account, amount):

        success = account.withdraw(amount)

        if not success:
            return False

        transaction = Transaction(
            transaction_id=2,
            transaction_type="WITHDRAWAL",
            amount=amount,
            source_account=account.account_number,
            destination_account=None,
            timestamp="2026-08-15 10:05:00",
            status="COMPLETED"
        )

        self.bank.add_transaction(transaction)

        return True