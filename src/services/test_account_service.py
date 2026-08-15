from src.infrastructure.database.database import SessionLocal
from src.repositories.account_repository import AccountRepository
from src.services.account_service import AccountService


def main():
    db = SessionLocal()

    try:
        repository = AccountRepository(db)
        service = AccountService(repository)

        account = service.create_account(
            customer_id=1,
            customer=None,
            account_type="SAVINGS",
            initial_balance=50000,
            status="ACTIVE"
        )

        print("\nAccount created through service:")
        print(account.account_number)
        print(account.customer_id)
        print(account.balance)
        print(account.account_type)

        found = service.get_account(
            account.account_number
        )

        print("\nAccount fetched through service:")
        print(found.account_number)
        print(found.balance)
        print(found.account_type)

    finally:
        db.close()


if __name__ == "__main__":
    main()