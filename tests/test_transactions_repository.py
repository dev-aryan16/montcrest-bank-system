from src.repositories.customer_repository import CustomerRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository


def test_create_transaction(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9100001,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    db_session.commit()

    transaction = transaction_repository.create({
        "transaction_id": "TXN900001",
        "transaction_type": "DEPOSIT",
        "amount": 5000,
        "source_account": None,
        "destination_account": account.account_number,
        "status": "COMPLETED",
        "description": "Test deposit"
    })

    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.transaction_id == "TXN900001"
    assert transaction.transaction_type == "DEPOSIT"
    assert transaction.amount == 5000
    assert transaction.destination_account == account.account_number
    assert transaction.status == "COMPLETED"


def test_get_transaction_by_id(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9100002,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    db_session.commit()

    transaction = transaction_repository.create({
        "transaction_id": "TXN900002",
        "transaction_type": "WITHDRAWAL",
        "amount": 2000,
        "source_account": account.account_number,
        "destination_account": None,
        "status": "COMPLETED",
        "description": "Test withdrawal"
    })

    db_session.commit()

    found = transaction_repository.get_by_id(
        "TXN900002"
    )

    assert found is not None
    assert found.transaction_id == "TXN900002"
    assert found.source_account == account.account_number


def test_get_account_transactions(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9100003,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    db_session.commit()

    first = transaction_repository.create({
        "transaction_id": "TXN900003",
        "transaction_type": "DEPOSIT",
        "amount": 5000,
        "destination_account": account.account_number,
        "status": "COMPLETED"
    })

    second = transaction_repository.create({
        "transaction_id": "TXN900004",
        "transaction_type": "WITHDRAWAL",
        "amount": 1000,
        "source_account": account.account_number,
        "status": "COMPLETED"
    })

    db_session.commit()

    transactions = transaction_repository.get_by_account(
        account.account_number
    )

    transaction_ids = {
        transaction.transaction_id
        for transaction in transactions
    }

    assert first.transaction_id in transaction_ids
    assert second.transaction_id in transaction_ids