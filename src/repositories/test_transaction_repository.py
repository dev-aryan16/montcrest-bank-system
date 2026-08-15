from src.infrastructure.database.database import SessionLocal
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository


def main():
    db = SessionLocal()

    try:
        account_repository = AccountRepository(db)
        transaction_repository = TransactionRepository(db)

        # 1. Find source account
        source_account = account_repository.get_by_account_number(
            1000001
        )

        if source_account is None:
            print("Source account not found.")
            return

        print("\nSource account:")
        print(
            source_account.account_number,
            source_account.balance
        )

        # 2. Create a transaction
        transaction = transaction_repository.create({
            "transaction_id": "TXN000001",
            "transaction_type": "DEPOSIT",
            "amount": 10000,
            "source_account": None,
            "destination_account": source_account.account_number,
            "status": "COMPLETED",
            "description": "Test deposit"
        })

        print("\nTransaction created:")
        print(transaction.transaction_id)
        print(transaction.transaction_type)
        print(transaction.amount)
        print(transaction.destination_account)

        # 3. Fetch transaction by ID
        found_transaction = transaction_repository.get_by_id(
            "TXN000001"
        )

        print("\nTransaction fetched:")
        print(found_transaction.transaction_id)
        print(found_transaction.transaction_type)
        print(found_transaction.amount)

        # 4. Fetch transactions for account
        transactions = transaction_repository.get_by_account(
            source_account.account_number
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