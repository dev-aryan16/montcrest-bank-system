class Transaction:
    def __init__(self, transaction_id, transaction_type, amount, source_account, destination_account, timestamp, status):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.source_account = source_account
        self.destination_account = destination_account
        self.timestamp = timestamp
        self.status = status


    def get_transaction_info(self):
        return{
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "source_account": self.source_account,
            "destination_account": self.destination_account,
            "timestamp": self.timestamp,
            "status": self.status
        }