class Role:

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name
        self.permissions = []

    def add_permission(self, permission):
        self.permissions.append(permission)

    def remove_permission(self, permission):
        if permission in self.permissions:
            self.permissions.remove(permission)

    def has_permission(self, permission_code):
        for permission in self.permissions:
            if permission.code == permission_code:
                return True
        return False

    def get_role_info(self):
        return {
            "role_id": self.role_id,
            "name": self.name,
            "permissions": [
                permission.code
                for permission in self.permissions
            ]
        }