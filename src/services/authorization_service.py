class AuthorizationService:

    def has_permission(self, user, permission_code):
        return user.has_permission(permission_code)

    def check_permission(self, user, permission_code):
        if not user.has_permission(permission_code):
            raise PermissionError(
                f"User does not have permission: {permission_code}"
            )

        return True