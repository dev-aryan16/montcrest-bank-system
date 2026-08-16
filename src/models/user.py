class User:

    def __init__(
        self,
        user_id,
        username,
        password_hash,
        customer,
        status="INACTIVE"
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.customer = customer
        self.status = status
        self.roles = []

    def activate(self):
        self.status = "ACTIVE"

    def deactivate(self):
        self.status = "INACTIVE"

    def lock(self):
        self.status = "LOCKED"

    def assign_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)

    def has_permission(self, permission_code):
        for role in self.roles:
            if role.has_permission(permission_code):
                return True

        return False

    def get_user_info(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "customer": self.customer.get_full_name(),
            "status": self.status,
            "roles": [role.name for role in self.roles]
        }