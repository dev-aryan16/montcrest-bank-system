from src.infrastructure.database.database import SessionLocal
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.transfer_service import TransferService


def main():
    db = SessionLocal()

    try:
        account_repository = AccountRepository(db)
        transaction_repository = TransactionRepository(db)

        transfer_service = TransferService(
            account_repository,
            transaction_repository
        )

        source = account_repository.get_by_account_number(
            1000001
        )

        destination = account_repository.get_by_account_number(
            1000002
        )

        if source is None:
            print("Source account 1000001 not found.")
            return

        if destination is None:
            print("Destination account 1000002 not found.")
            return

        print("\nBefore transfer:")
        print("Source:", source.account_number, source.balance)
        print(
            "Destination:",
            destination.account_number,
            destination.balance
        )

        transaction = transfer_service.transfer(
            source_account_number=1000001,
            destination_account_number=1000002,
            amount=5000
        )

        print("\nTransfer successful:")
        print(transaction.transaction_id)
        print(transaction.transaction_type)
        print(transaction.amount)
        print(transaction.status)

        # Read fresh values from database
        updated_source = account_repository.get_by_account_number(
            1000001
        )

        updated_destination = account_repository.get_by_account_number(
            1000002
        )

        print("\nAfter transfer:")
        print(
            "Source:",
            updated_source.account_number,
            updated_source.balance
        )

        print(
            "Destination:",
            updated_destination.account_number,
            updated_destination.balance
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()