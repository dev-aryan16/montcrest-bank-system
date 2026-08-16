from src.models.kyc_profile import KYCProfile
from src.services.kyc_service import KYCService


class DummyCustomer:

    def __init__(self):
        self.name = "Test Customer"
        self.kyc_profile = None
        self.status = "INACTIVE"

    def get_full_name(self):
        return self.name


def test_create_kyc_profile():
    customer = DummyCustomer()
    service = KYCService()

    profile = service.create_kyc_profile(
        customer=customer,
        kyc_id=1,
        document_type="PASSPORT",
        document_number="P1234567"
    )

    assert profile is not None
    assert profile.kyc_id == 1
    assert profile.customer == customer
    assert profile.document_type == "PASSPORT"
    assert profile.document_number == "P1234567"
    assert profile.status == "PENDING"

    assert customer.kyc_profile is profile


def test_kyc_initial_status():
    customer = DummyCustomer()

    profile = KYCProfile(
        kyc_id=2,
        customer=customer,
        document_type="AADHAAR",
        document_number="123456789012"
    )

    assert profile.status == "PENDING"
    assert profile.verified_at is None


def test_verify_kyc():
    customer = DummyCustomer()
    service = KYCService()

    service.create_kyc_profile(
        customer=customer,
        kyc_id=3,
        document_type="PAN",
        document_number="ABCDE1234F"
    )

    result = service.verify_kyc(customer)

    assert result is True
    assert customer.kyc_profile.status == "VERIFIED"
    assert customer.kyc_profile.verified_at is not None
    assert customer.status == "ACTIVE"


def test_reject_kyc():
    customer = DummyCustomer()
    service = KYCService()

    service.create_kyc_profile(
        customer=customer,
        kyc_id=4,
        document_type="PASSPORT",
        document_number="P9876543"
    )

    result = service.reject_kyc(customer)

    assert result is True
    assert customer.kyc_profile.status == "REJECTED"
    assert customer.kyc_profile.verified_at is None
    assert customer.status == "INACTIVE"


def test_get_kyc_status():
    customer = DummyCustomer()
    service = KYCService()

    service.create_kyc_profile(
        customer=customer,
        kyc_id=5,
        document_type="DRIVING_LICENSE",
        document_number="DL123456789"
    )

    assert service.get_kyc_status(customer) == "PENDING"

    service.verify_kyc(customer)

    assert service.get_kyc_status(customer) == "VERIFIED"


def test_verify_kyc_without_profile():
    customer = DummyCustomer()
    service = KYCService()

    result = service.verify_kyc(customer)

    assert result is False
    assert customer.status == "INACTIVE"


def test_reject_kyc_without_profile():
    customer = DummyCustomer()
    service = KYCService()

    result = service.reject_kyc(customer)

    assert result is False
    assert customer.status == "INACTIVE"


def test_get_kyc_status_without_profile():
    customer = DummyCustomer()
    service = KYCService()

    assert service.get_kyc_status(customer) is None