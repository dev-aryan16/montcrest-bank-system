import pytest

from src.repositories.customer_repository import CustomerRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.transfer_service import TransferService


def test_transfer_rollback(
    db_session,
    customer_data
):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    customer = customer_repository.create(customer_data)

    source = account_repository.create({
        "account_number": 9300001,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    destination = account_repository.create({
        "account_number": 9300002,
        "customer_id": customer.customer_id,
        "balance": 25000,
        "account_type": "CURRENT",
        "status": "ACTIVE"
    })

    db_session.commit()

    source_before = source.balance
    destination_before = destination.balance

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    # Perform the balance changes inside the current session.
    source.balance -= 5000
    destination.balance += 5000

    account_repository.update(source)
    account_repository.update(destination)

    # Intentionally create a failure before commit.
    with pytest.raises(RuntimeError, match="Forced rollback"):
        raise RuntimeError("Forced rollback")

    # The above exception is outside TransferService's try/except,
    # so explicitly roll back the session.
    db_session.rollback()

    db_session.expire_all()

    source_after = account_repository.get_by_account_number(
        source.account_number
    )

    destination_after = account_repository.get_by_account_number(
        destination.account_number
    )

    assert source_after.balance == source_before
    assert destination_after.balance == destination_before