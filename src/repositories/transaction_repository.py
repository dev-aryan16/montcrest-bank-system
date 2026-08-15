from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.transaction_model import TransactionDB


class TransactionRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction_data):
        transaction = TransactionDB(
            transaction_id=transaction_data["transaction_id"],
            transaction_type=transaction_data["transaction_type"],
            amount=transaction_data["amount"],
            source_account=transaction_data.get("source_account"),
            destination_account=transaction_data.get("destination_account"),
            timestamp=transaction_data.get("timestamp"),
            status=transaction_data.get("status", "PENDING"),
            description=transaction_data.get("description")
        )

        self.session.add(transaction)

        return transaction

    def get_by_id(self, transaction_id):
        statement = select(TransactionDB).where(
            TransactionDB.transaction_id == transaction_id
        )

        return self.session.scalar(statement)

    def get_by_account(self, account_number):
        statement = (
            select(TransactionDB)
            .where(
                (TransactionDB.source_account == account_number)
                | (TransactionDB.destination_account == account_number)
            )
            .order_by(TransactionDB.timestamp.desc())
        )

        return self.session.scalars(statement).all()

    def get_all(self):
        statement = select(TransactionDB).order_by(
            TransactionDB.timestamp.desc()
        )

        return self.session.scalars(statement).all()

    def get_latest_transaction(self):
        statement = (
            select(TransactionDB)
            .order_by(TransactionDB.timestamp.desc())
            .limit(1)
        )

        return self.session.scalar(statement)

    def update(self, transaction):
        self.session.add(transaction)

        return transaction

    def delete(self, transaction_id):
        transaction = self.get_by_id(transaction_id)

        if transaction is None:
            return False

        self.session.delete(transaction)

        return True