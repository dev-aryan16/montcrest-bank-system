class Permission:

    def __init__(self, permission_id, code, description):
        self.permission_id = permission_id
        self.code = code
        self.description = description

    def get_permission_info(self):
        return {
            "permission_id": self.permission_id,
            "code": self.code,
            "description": self.description
        }