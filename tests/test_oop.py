from datetime import datetime
from inspect import isabstract

from src.models.account import BankAccount
from src.models.savings_account import SavingsAccount
from src.models.current_account import CurrentAccount
from src.models.fixed_deposit import FixedDepositAccount

from src.models.employee import Employee
from src.models.teller import Teller
from src.models.manager import Manager
from src.models.loan_officer import LoanOfficer
from src.models.administrator import Administrator

from src.models.transaction import Transaction


class DummyCustomer:

    def get_full_name(self):
        return "Test Customer"


def test_bank_account_is_abstract():
    assert isabstract(BankAccount)


def test_account_inheritance():
    assert issubclass(SavingsAccount, BankAccount)
    assert issubclass(CurrentAccount, BankAccount)
    assert issubclass(FixedDepositAccount, BankAccount)


def test_employee_inheritance():
    assert issubclass(Teller, Employee)
    assert issubclass(Manager, Employee)
    assert issubclass(LoanOfficer, Employee)
    assert issubclass(Administrator, Employee)


def test_transaction_creation():
    transaction = Transaction(
        transaction_type="TEST",
        amount=100
    )

    assert transaction.transaction_id.startswith("TXN")
    assert transaction.transaction_type == "TEST"
    assert transaction.amount == 100


def test_account_polymorphism():
    customer = DummyCustomer()
    created_at = datetime.now()

    accounts = [
        SavingsAccount(
            account_number=1,
            customer=customer,
            balance=10000,
            status="ACTIVE",
            created_at=created_at
        ),
        CurrentAccount(
            account_number=2,
            customer=customer,
            balance=10000,
            status="ACTIVE",
            created_at=created_at
        ),
        FixedDepositAccount(
            account_number=3,
            customer=customer,
            balance=10000,
            status="ACTIVE",
            created_at=created_at
        )
    ]

    results = [
        account.calculate_interest()
        for account in accounts
    ]

    assert len(results) == 3