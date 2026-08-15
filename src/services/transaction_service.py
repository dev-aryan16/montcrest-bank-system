from src.models.transaction import Transaction


class TransactionService:

    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    def create_transaction(
        self,
        transaction_type,
        amount,
        source_account=None,
        destination_account=None,
        status="COMPLETED",
        description="",
        commit=True
    ):
        try:
            latest_transaction = (
                self.transaction_repository.get_latest_transaction()
            )

            if latest_transaction is None:
                next_id = 1
            else:
                latest_number = int(
                    latest_transaction.transaction_id.replace(
                        "TXN",
                        ""
                    )
                )
                next_id = latest_number + 1

            transaction_id = f"TXN{next_id:06d}"

            transaction = Transaction(
                transaction_id=transaction_id,
                transaction_type=transaction_type,
                amount=amount,
                source_account=source_account,
                destination_account=destination_account,
                status=status,
                description=description
            )

            transaction_data = {
                "transaction_id": transaction.transaction_id,
                "transaction_type": transaction.transaction_type,
                "amount": transaction.amount,
                "source_account": transaction.source_account,
                "destination_account": transaction.destination_account,
                "timestamp": transaction.timestamp,
                "status": transaction.status,
                "description": transaction.description
            }

            transaction = self.transaction_repository.create(
                transaction_data
            )

            if commit:
                self.transaction_repository.session.commit()
                self.transaction_repository.session.refresh(
                    transaction
                )

            return transaction

        except Exception:
            if commit:
                self.transaction_repository.session.rollback()
            raise

    def process_deposit(self, account_number, amount):
        return self.create_transaction(
            transaction_type="DEPOSIT",
            amount=amount,
            destination_account=account_number,
            status="COMPLETED",
            description="Cash deposit"
        )

    def process_withdrawal(self, account_number, amount):
        return self.create_transaction(
            transaction_type="WITHDRAWAL",
            amount=amount,
            source_account=account_number,
            status="COMPLETED",
            description="Cash withdrawal"
        )

    def get_transaction(self, transaction_id):
        transaction = self.transaction_repository.get_by_id(
            transaction_id
        )

        if transaction is None:
            raise ValueError(
                f"Transaction {transaction_id} not found."
            )

        return transaction

    def get_account_transactions(self, account_number):
        return self.transaction_repository.get_by_account(
            account_number
        )

    def get_all_transactions(self):
        return self.transaction_repository.get_all()