from src.services.transaction_service import TransactionService


class TransferService:

    def __init__(
        self,
        account_repository,
        transaction_repository
    ):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transaction_service = TransactionService(
            transaction_repository
        )

    def transfer(
        self,
        source_account_number,
        destination_account_number,
        amount
    ):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")

        if source_account_number == destination_account_number:
            raise ValueError(
                "Source and destination accounts cannot be the same."
            )

        session = self.account_repository.session

        try:
            # 1. Get both accounts
            source_account = (
                self.account_repository.get_by_account_number(
                    source_account_number
                )
            )

            destination_account = (
                self.account_repository.get_by_account_number(
                    destination_account_number
                )
            )

            if source_account is None:
                raise ValueError(
                    f"Source account {source_account_number} not found."
                )

            if destination_account is None:
                raise ValueError(
                    f"Destination account "
                    f"{destination_account_number} not found."
                )

            # 2. Validate accounts
            if source_account.status != "ACTIVE":
                raise ValueError(
                    "Source account is not active."
                )

            if destination_account.status != "ACTIVE":
                raise ValueError(
                    "Destination account is not active."
                )

            # 3. Check balance
            if amount > source_account.balance:
                raise ValueError(
                    "Insufficient balance."
                )

            # 4. Update balances
            source_account.balance -= amount
            destination_account.balance += amount

            self.account_repository.update(source_account)
            self.account_repository.update(destination_account)

            # 5. Create transaction record
            latest_transaction = (
                self.transaction_repository
                .get_latest_transaction()
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

            transaction = self.transaction_service.create_transaction(
                transaction_type="TRANSFER",
                amount=amount,
                source_account=source_account_number,
                destination_account=destination_account_number,
                status="COMPLETED",
                description="Account-to-account transfer"
            )

            # 6. Commit everything together
            session.commit()

            session.refresh(source_account)
            session.refresh(destination_account)

            return transaction

        except Exception:
            session.rollback()
            raise