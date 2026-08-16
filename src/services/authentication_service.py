import bcrypt

from src.services.session_service import SessionService

class AuthenticationService:

    def __init__(self):
        self.session_service = SessionService()

    def hash_password(self, password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password, password_hash):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )

    def authenticate(self, user, password):

        if user.status == "LOCKED":
            return None

        password_valid = self.verify_password(
            password,
            user.password_hash
        )

        if not password_valid:
            return None

        user.activate()

        session = self.session_service.create_session(user)

        return session

    def logout(self, session):

        if not session.is_valid():
            return False

        self.session_service.revoke_session(session)

        return True