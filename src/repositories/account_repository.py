from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.account_model import AccountDB


class AccountRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, account_data):
        account = AccountDB(
            account_number=account_data["account_number"],
            customer_id=account_data["customer_id"],
            balance=account_data.get("balance", 0),
            account_type=account_data["account_type"],
            status=account_data.get("status", "ACTIVE")
        )

        self.session.add(account)
        return account

    def get_by_account_number(self, account_number):
        statement = select(AccountDB).where(
            AccountDB.account_number == account_number
        )

        return self.session.scalar(statement)

    def get_by_customer_id(self, customer_id):
        statement = (
            select(AccountDB)
            .where(AccountDB.customer_id == customer_id)
            .order_by(AccountDB.account_number)
        )

        return self.session.scalars(statement).all()

    def get_all(self):
        statement = select(AccountDB).order_by(
            AccountDB.account_number
        )

        return self.session.scalars(statement).all()

    def update(self, account):
        self.session.add(account)
        return account

    def delete(self, account_number):
        account = self.get_by_account_number(account_number)

        if account is None:
            return False

        self.session.delete(account)
        return True