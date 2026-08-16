import pytest

from datetime import datetime

from src.models.savings_account import SavingsAccount
from src.models.current_account import CurrentAccount
from src.models.fixed_deposit import FixedDepositAccount


class DummyCustomer:

    def get_full_name(self):
        return "Test Customer"


def test_savings_account_rejects_negative_deposit():
    account = SavingsAccount(
        account_number=1,
        customer=DummyCustomer(),
        balance=10000,
        status="ACTIVE",
        created_at=datetime.now()
    )

    with pytest.raises(Exception):
        account.deposit(-1000)


def test_savings_account_rejects_zero_deposit():
    account = SavingsAccount(
        account_number=2,
        customer=DummyCustomer(),
        balance=10000,
        status="ACTIVE",
        created_at=datetime.now()
    )

    with pytest.raises(Exception):
        account.deposit(0)


def test_withdrawal_cannot_exceed_balance():
    account = SavingsAccount(
        account_number=3,
        customer=DummyCustomer(),
        balance=10000,
        status="ACTIVE",
        created_at=datetime.now()
    )

    with pytest.raises(Exception):
        account.withdraw(20000)


def test_valid_deposit_changes_balance():
    account = SavingsAccount(
        account_number=4,
        customer=DummyCustomer(),
        balance=10000,
        status="ACTIVE",
        created_at=datetime.now()
    )

    account.deposit(5000)

    assert account.balance == 15000


def test_valid_withdrawal_changes_balance():
    account = SavingsAccount(
        account_number=5,
        customer=DummyCustomer(),
        balance=10000,
        status="ACTIVE",
        created_at=datetime.now()
    )

    account.withdraw(3000)

    assert account.balance == 7000