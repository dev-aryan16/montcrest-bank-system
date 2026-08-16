from datetime import datetime

from src.models.beneficiary import Beneficiary
from src.services.beneficiary_service import BeneficiaryService


class DummyCustomer:

    def __init__(self):
        self.name = "Test Customer"
        self.beneficiaries = []

    def get_full_name(self):
        return self.name


def create_beneficiary(customer):
    return Beneficiary(
        beneficiary_id=1,
        owner_customer=customer,
        beneficiary_name="John Doe",
        account_number=1234567890,
        bank_name="Montcrest Bank",
        nickname="John",
        status="ACTIVE",
        created_at=datetime.now()
    )


def test_beneficiary_creation():
    customer = DummyCustomer()

    beneficiary = create_beneficiary(customer)

    assert beneficiary.beneficiary_id == 1
    assert beneficiary.owner_customer == customer
    assert beneficiary.beneficiary_name == "John Doe"
    assert beneficiary.account_number == 1234567890
    assert beneficiary.bank_name == "Montcrest Bank"
    assert beneficiary.nickname == "John"
    assert beneficiary.status == "ACTIVE"


def test_get_beneficiary_info():
    customer = DummyCustomer()

    beneficiary = create_beneficiary(customer)

    info = beneficiary.get_beneficiary_info()

    assert info["beneficiary_id"] == 1
    assert info["owner_customer"] == "Test Customer"
    assert info["beneficiary_name"] == "John Doe"
    assert info["account_number"] == 1234567890
    assert info["bank_name"] == "Montcrest Bank"
    assert info["nickname"] == "John"
    assert info["status"] == "ACTIVE"


def test_deactivate_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    beneficiary = create_beneficiary(customer)

    service.add_beneficiary(customer, beneficiary)

    result = service.deactivate_beneficiary(
        customer,
        beneficiary.beneficiary_id
    )

    assert result is True
    assert beneficiary.status == "INACTIVE"


def test_activate_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    beneficiary = create_beneficiary(customer)
    beneficiary.deactivate()

    service.add_beneficiary(customer, beneficiary)

    result = service.activate_beneficiary(
        customer,
        beneficiary.beneficiary_id
    )

    assert result is True
    assert beneficiary.status == "ACTIVE"


def test_find_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    beneficiary = create_beneficiary(customer)

    service.add_beneficiary(customer, beneficiary)

    found = service.find_beneficiary(
        customer,
        beneficiary.beneficiary_id
    )

    assert found is beneficiary


def test_find_missing_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    found = service.find_beneficiary(
        customer,
        999
    )

    assert found is None


def test_deactivate_missing_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    result = service.deactivate_beneficiary(
        customer,
        999
    )

    assert result is False


def test_activate_missing_beneficiary():
    customer = DummyCustomer()
    service = BeneficiaryService()

    result = service.activate_beneficiary(
        customer,
        999
    )

    assert result is False