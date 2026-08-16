from src.models.permission import Permission
from src.models.role import Role


class RBACService:

    def __init__(self):
        self.permissions = {}
        self.roles = {}

        self._create_permissions()
        self._create_roles()

    def _create_permissions(self):

        permission_data = [
            (1, "VIEW_ACCOUNT", "View account information"),
            (2, "DEPOSIT", "Perform deposit operations"),
            (3, "WITHDRAW", "Perform withdrawal operations"),
            (4, "TRANSFER", "Perform account transfers"),
            (5, "MANAGE_BENEFICIARY", "Manage beneficiaries"),
            (6, "VIEW_STATEMENT", "View account statements"),
            (7, "MANAGE_CUSTOMERS", "Manage customer information"),
            (8, "APPROVE_TRANSACTIONS", "Approve banking transactions"),
            (9, "APPROVE_LOANS", "Approve loan applications"),
            (10, "PROCESS_LOANS", "Process loan applications"),
            (11, "MANAGE_EMPLOYEES", "Manage bank employees"),
            (12, "MANAGE_BRANCH", "Manage branch operations"),
            (13, "SYSTEM_ADMIN", "Perform system administration"),
        ]

        for permission_id, code, description in permission_data:
            permission = Permission(
                permission_id=permission_id,
                code=code,
                description=description
            )

            self.permissions[code] = permission

    def _create_roles(self):

        role_permissions = {
            "TELLER": [
                "VIEW_ACCOUNT",
                "DEPOSIT",
                "WITHDRAW",
                "VIEW_STATEMENT"
            ],

            "MANAGER": [
                "VIEW_ACCOUNT",
                "DEPOSIT",
                "WITHDRAW",
                "TRANSFER",
                "VIEW_STATEMENT",
                "MANAGE_CUSTOMERS",
                "APPROVE_TRANSACTIONS",
                "APPROVE_LOANS"
            ],

            "LOAN_OFFICER": [
                "VIEW_ACCOUNT",
                "VIEW_STATEMENT",
                "PROCESS_LOANS",
                "APPROVE_LOANS"
            ],

            "ADMINISTRATOR": [
                "MANAGE_CUSTOMERS",
                "MANAGE_EMPLOYEES",
                "MANAGE_BRANCH",
                "SYSTEM_ADMIN"
            ]
        }

        role_id = 1

        for role_name, permission_codes in role_permissions.items():

            role = Role(
                role_id=role_id,
                name=role_name
            )

            for permission_code in permission_codes:
                role.add_permission(
                    self.permissions[permission_code]
                )

            self.roles[role_name] = role
            role_id += 1

    def get_role(self, role_name):
        return self.roles.get(role_name.upper())

    def get_permission(self, permission_code):
        return self.permissions.get(permission_code.upper())