from src.models.session import Session
from src.services.session_service import SessionService


class DummyUser:

    def __init__(self):
        self.username = "testuser"


def test_create_session():
    service = SessionService()
    user = DummyUser()

    session = service.create_session(user)

    assert session is not None
    assert session.session_id == "SESSION000001"
    assert session.user == user
    assert session.status == "ACTIVE"


def test_validate_active_session():
    service = SessionService()
    user = DummyUser()

    session = service.create_session(user)

    assert service.validate_session(session) is True


def test_revoke_session():
    service = SessionService()
    user = DummyUser()

    session = service.create_session(user)

    result = service.revoke_session(session)

    assert result is True
    assert session.status == "REVOKED"
    assert service.validate_session(session) is False


def test_get_session():
    service = SessionService()
    user = DummyUser()

    session = service.create_session(user)

    found = service.get_session(session.session_id)

    assert found is session


def test_get_missing_session():
    service = SessionService()

    found = service.get_session("SESSION999999")

    assert found is None


def test_get_user_sessions():
    service = SessionService()
    user = DummyUser()
    another_user = DummyUser()
    another_user.username = "anotheruser"

    first_session = service.create_session(user)
    second_session = service.create_session(user)
    other_session = service.create_session(another_user)

    user_sessions = service.get_user_sessions(user)

    assert first_session in user_sessions
    assert second_session in user_sessions
    assert other_session not in user_sessions


def test_expired_session():
    session = Session(
        session_id="SESSION000001",
        user=DummyUser(),
        duration_minutes=-1
    )

    assert session.is_valid() is False
    assert session.status == "EXPIRED"


def test_session_info():
    service = SessionService()
    user = DummyUser()

    session = service.create_session(user)

    info = session.get_session_info()

    assert info["session_id"] == session.session_id
    assert info["user"] == "testuser"
    assert info["status"] == "ACTIVE"