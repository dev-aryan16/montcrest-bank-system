from src.utils.generators import IDGenerator, TimestampGenerator


class Transaction:

    def __init__(
        self,
        transaction_type,
        amount,
        source_account=None,
        destination_account=None,
        status="PENDING",
        description="",
        transaction_id=None
    ):
        if transaction_id is None:
            self.transaction_id = IDGenerator.generate_transaction_id()
        else:
            self.transaction_id = transaction_id

        self.transaction_type = transaction_type
        self.amount = amount
        self.source_account = source_account
        self.destination_account = destination_account
        self.timestamp = TimestampGenerator.generate_timestamp()
        self.status = status
        self.description = description

    def get_transaction_info(self):
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "source_account": self.source_account,
            "destination_account": self.destination_account,
            "timestamp": self.timestamp,
            "status": self.status,
            "description": self.description
        }