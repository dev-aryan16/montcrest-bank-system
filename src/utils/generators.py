from datetime import datetime


class IDGenerator:

    _transaction_counter = 0

    @classmethod
    def generate_transaction_id(cls):
        cls._transaction_counter += 1
        return f"TXN{cls._transaction_counter:06d}"


class TimestampGenerator:

    @staticmethod
    def generate_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")