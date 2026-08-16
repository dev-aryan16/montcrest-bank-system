from src.repositories.customer_repository import CustomerRepository
from src.repositories.account_repository import AccountRepository


def test_create_account(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9000001,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    db_session.commit()
    db_session.refresh(account)

    assert account.account_number == 9000001
    assert account.customer_id == customer.customer_id
    assert account.balance == 50000
    assert account.account_type == "SAVINGS"


def test_get_account_by_number(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9000002,
        "customer_id": customer.customer_id,
        "balance": 25000,
        "account_type": "CURRENT",
        "status": "ACTIVE"
    })

    db_session.commit()

    found = account_repository.get_by_account_number(9000002)

    assert found is not None
    assert found.account_number == 9000002
    assert found.customer_id == customer.customer_id


def test_get_accounts_by_customer(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)

    customer = customer_repository.create(customer_data)

    first = account_repository.create({
        "account_number": 9000003,
        "customer_id": customer.customer_id,
        "balance": 10000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    second = account_repository.create({
        "account_number": 9000004,
        "customer_id": customer.customer_id,
        "balance": 20000,
        "account_type": "CURRENT",
        "status": "ACTIVE"
    })

    db_session.commit()

    accounts = account_repository.get_by_customer_id(
        customer.customer_id
    )

    account_numbers = {
        account.account_number
        for account in accounts
    }

    assert first.account_number in account_numbers
    assert second.account_number in account_numbers


def test_customer_account_relationship(db_session, customer_data):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)

    customer = customer_repository.create(customer_data)

    account = account_repository.create({
        "account_number": 9000005,
        "customer_id": customer.customer_id,
        "balance": 10000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    db_session.commit()
    db_session.refresh(customer)

    assert account.customer_id == customer.customer_id
    assert account.customer.customer_id == customer.customer_id