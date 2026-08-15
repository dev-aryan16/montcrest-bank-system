from sqlalchemy import text

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

        # Get balances before the failed transfer
        source = account_repository.get_by_account_number(1000001)
        destination = account_repository.get_by_account_number(1000002)

        source_before = source.balance
        destination_before = destination.balance

        print("\nBefore rollback test:")
        print("Source:", source_before)
        print("Destination:", destination_before)

        try:
            # Start a manual transaction operation
            source.balance -= 5000
            destination.balance += 5000

            account_repository.update(source)
            account_repository.update(destination)

            # Add a transaction record
            transaction_service = transfer_service.transaction_service

            transaction_service.create_transaction(
                transaction_type="TRANSFER",
                amount=5000,
                source_account=1000001,
                destination_account=1000002,
                status="COMPLETED",
                description="Rollback test",
                commit=False
            )

            # Force an error before commit
            raise RuntimeError("Forced failure for rollback test")

        except Exception as error:
            print("\nExpected error:")
            print(error)

            db.rollback()
            print("ROLLBACK executed.")

        # Read fresh values after rollback
        db.expire_all()

        source_after = account_repository.get_by_account_number(
            1000001
        )

        destination_after = account_repository.get_by_account_number(
            1000002
        )

        print("\nAfter rollback:")
        print("Source:", source_after.balance)
        print("Destination:", destination_after.balance)

        # Verify balances were restored
        if (
            source_after.balance == source_before
            and destination_after.balance == destination_before
        ):
            print("\nRollback successful: balances restored.")
        else:
            print("\nRollback FAILED: balances changed.")

        # Verify the rollback test transaction was not persisted
        result = db.execute(
            text("""
                SELECT COUNT(*)
                FROM transactions
                WHERE description = 'Rollback test'
            """)
        )

        transaction_count = result.scalar()

        if transaction_count == 0:
            print(
                "Rollback successful: test transaction was not persisted."
            )
        else:
            print(
                "Rollback FAILED: test transaction still exists."
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()