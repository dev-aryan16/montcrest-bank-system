from datetime import datetime

from src.models.session import Session


class SessionService:

    def __init__(self):
        self.sessions = []
        self._session_counter = 0

    def create_session(self, user):
        self._session_counter += 1

        session_id = f"SESSION{self._session_counter:06d}"

        session = Session(
            session_id=session_id,
            user=user
        )

        self.sessions.append(session)

        return session

    def validate_session(self, session):
        return session.is_valid()

    def revoke_session(self, session):
        session.revoke()
        return True

    def get_session(self, session_id):
        for session in self.sessions:
            if session.session_id == session_id:
                return session

        return None

    def get_user_sessions(self, user):
        return [
            session
            for session in self.sessions
            if session.user == user
        ]

    def cleanup_expired_sessions(self):
        for session in self.sessions:
            session.is_valid()