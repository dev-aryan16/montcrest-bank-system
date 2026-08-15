from src.infrastructure.database.database import SessionLocal
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService


def main():
    db = SessionLocal()

    try:
        repository = TransactionRepository(db)
        service = TransactionService(repository)

        # 1. Create a deposit transaction
        transaction = service.process_deposit(
            account_number=1000001,
            amount=5000
        )

        print("\nTransaction created through service:")
        print(transaction.transaction_id)
        print(transaction.transaction_type)
        print(transaction.amount)
        print(transaction.destination_account)
        print(transaction.status)

        # 2. Fetch the transaction
        found = service.get_transaction(
            transaction.transaction_id
        )

        print("\nTransaction fetched through service:")
        print(found.transaction_id)
        print(found.transaction_type)
        print(found.amount)
        print(found.status)

        # 3. Fetch account transaction history
        transactions = service.get_account_transactions(
            1000001
        )

        print("\nAccount transaction history:")

        for item in transactions:
            print(
                item.transaction_id,
                item.transaction_type,
                item.amount,
                item.status
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()