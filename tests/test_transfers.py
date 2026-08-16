import pytest

from src.repositories.customer_repository import CustomerRepository
from src.repositories.account_repository import AccountRepository
from src.repositories.transaction_repository import TransactionRepository
from src.services.transfer_service import TransferService


def create_test_accounts(db_session, customer_data, base_number):
    customer_repository = CustomerRepository(db_session)
    account_repository = AccountRepository(db_session)

    customer = customer_repository.create(customer_data)

    source = account_repository.create({
        "account_number": base_number,
        "customer_id": customer.customer_id,
        "balance": 50000,
        "account_type": "SAVINGS",
        "status": "ACTIVE"
    })

    destination = account_repository.create({
        "account_number": base_number + 1,
        "customer_id": customer.customer_id,
        "balance": 25000,
        "account_type": "CURRENT",
        "status": "ACTIVE"
    })

    db_session.commit()

    return source, destination


def test_successful_transfer(
    db_session,
    customer_data
):
    source, destination = create_test_accounts(
        db_session,
        customer_data,
        9200001
    )

    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    transaction = transfer_service.transfer(
        source_account_number=source.account_number,
        destination_account_number=destination.account_number,
        amount=10000
    )

    updated_source = account_repository.get_by_account_number(
        source.account_number
    )

    updated_destination = account_repository.get_by_account_number(
        destination.account_number
    )

    assert updated_source.balance == 40000
    assert updated_destination.balance == 35000

    assert transaction.transaction_type == "TRANSFER"
    assert transaction.amount == 10000
    assert transaction.status == "COMPLETED"


def test_transfer_rejects_insufficient_balance(
    db_session,
    customer_data
):
    source, destination = create_test_accounts(
        db_session,
        customer_data,
        9200011
    )

    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    with pytest.raises(
        ValueError,
        match="Insufficient balance."
    ):
        transfer_service.transfer(
            source_account_number=source.account_number,
            destination_account_number=destination.account_number,
            amount=100000
        )


def test_transfer_rejects_same_account(
    db_session,
    customer_data
):
    source, _ = create_test_accounts(
        db_session,
        customer_data,
        9200021
    )

    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    with pytest.raises(
        ValueError,
        match="Source and destination accounts cannot be the same."
    ):
        transfer_service.transfer(
            source_account_number=source.account_number,
            destination_account_number=source.account_number,
            amount=1000
        )


def test_transfer_rejects_missing_source_account(
    db_session,
    customer_data
):
    _, destination = create_test_accounts(
        db_session,
        customer_data,
        9200031
    )

    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    with pytest.raises(
        ValueError,
        match="Source account 9999999 not found."
    ):
        transfer_service.transfer(
            source_account_number=9999999,
            destination_account_number=destination.account_number,
            amount=1000
        )


def test_transfer_rejects_missing_destination_account(
    db_session,
    customer_data
):
    source, _ = create_test_accounts(
        db_session,
        customer_data,
        9200041
    )

    account_repository = AccountRepository(db_session)
    transaction_repository = TransactionRepository(db_session)

    transfer_service = TransferService(
        account_repository,
        transaction_repository
    )

    with pytest.raises(
        ValueError,
        match="Destination account 9999999 not found."
    ):
        transfer_service.transfer(
            source_account_number=source.account_number,
            destination_account_number=9999999,
            amount=1000
        )