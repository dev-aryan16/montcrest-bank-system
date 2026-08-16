from src.models.user import User
from src.services.authentication_service import AuthenticationService


class DummyCustomer:

    def get_full_name(self):
        return "Test Customer"


def create_test_user(auth_service):
    password = "Password123"

    user = User(
        user_id=1,
        username="testuser",
        password_hash=auth_service.hash_password(password),
        customer=DummyCustomer(),
        status="ACTIVE"
    )

    return user, password


def test_hash_password():
    auth_service = AuthenticationService()

    password = "Password123"
    password_hash = auth_service.hash_password(password)

    assert password_hash != password
    assert isinstance(password_hash, str)


def test_verify_correct_password():
    auth_service = AuthenticationService()

    password = "Password123"
    password_hash = auth_service.hash_password(password)

    assert auth_service.verify_password(
        password,
        password_hash
    ) is True


def test_verify_wrong_password():
    auth_service = AuthenticationService()

    password_hash = auth_service.hash_password(
        "Password123"
    )

    assert auth_service.verify_password(
        "WrongPassword",
        password_hash
    ) is False


def test_locked_user_cannot_authenticate():
    auth_service = AuthenticationService()

    user, password = create_test_user(auth_service)
    user.lock()

    session = auth_service.authenticate(
        user,
        password
    )

    assert session is None


def test_invalid_password_cannot_authenticate():
    auth_service = AuthenticationService()

    user, _ = create_test_user(auth_service)

    session = auth_service.authenticate(
        user,
        "WrongPassword"
    )

    assert session is None


def test_successful_authentication():
    auth_service = AuthenticationService()

    user, password = create_test_user(auth_service)

    session = auth_service.authenticate(
        user,
        password
    )

    assert session is not None
    assert user.status == "ACTIVE"


def test_logout():
    auth_service = AuthenticationService()

    user, password = create_test_user(auth_service)

    session = auth_service.authenticate(
        user,
        password
    )

    assert session is not None

    result = auth_service.logout(session)

    assert result is True