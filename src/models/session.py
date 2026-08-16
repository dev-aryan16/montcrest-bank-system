from datetime import datetime, timedelta


class Session:

    def __init__(
        self,
        session_id,
        user,
        duration_minutes=30
    ):
        self.session_id = session_id
        self.user = user
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(
            minutes=duration_minutes
        )
        self.status = "ACTIVE"

    def is_valid(self):
        if self.status != "ACTIVE":
            return False

        if datetime.now() >= self.expires_at:
            self.status = "EXPIRED"
            return False

        return True

    def revoke(self):
        self.status = "REVOKED"

    def get_session_info(self):
        return {
            "session_id": self.session_id,
            "user": self.user.username,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": self.expires_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }