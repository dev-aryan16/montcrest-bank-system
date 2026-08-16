from src.models.user import User
from src.models.permission import Permission
from src.models.role import Role
from src.services.rbac_service import RBACService
from src.services.authorization_service import AuthorizationService


class DummyCustomer:

    def get_full_name(self):
        return "Test Customer"


def create_user():
    return User(
        user_id=1,
        username="testuser",
        password_hash="dummy_hash",
        customer=DummyCustomer(),
        status="ACTIVE"
    )


def test_permission_creation():
    rbac = RBACService()

    permission = rbac.get_permission("VIEW_ACCOUNT")

    assert permission is not None
    assert permission.code == "VIEW_ACCOUNT"
    assert permission.description == "View account information"


def test_role_creation():
    rbac = RBACService()

    role = rbac.get_role("TELLER")

    assert role is not None
    assert role.name == "TELLER"


def test_teller_permissions():
    rbac = RBACService()

    role = rbac.get_role("TELLER")

    assert role.has_permission("VIEW_ACCOUNT")
    assert role.has_permission("DEPOSIT")
    assert role.has_permission("WITHDRAW")
    assert role.has_permission("VIEW_STATEMENT")

    assert not role.has_permission("TRANSFER")
    assert not role.has_permission("MANAGE_EMPLOYEES")


def test_manager_permissions():
    rbac = RBACService()

    role = rbac.get_role("MANAGER")

    assert role.has_permission("VIEW_ACCOUNT")
    assert role.has_permission("DEPOSIT")
    assert role.has_permission("WITHDRAW")
    assert role.has_permission("TRANSFER")
    assert role.has_permission("MANAGE_CUSTOMERS")
    assert role.has_permission("APPROVE_TRANSACTIONS")
    assert role.has_permission("APPROVE_LOANS")


def test_loan_officer_permissions():
    rbac = RBACService()

    role = rbac.get_role("LOAN_OFFICER")

    assert role.has_permission("VIEW_ACCOUNT")
    assert role.has_permission("VIEW_STATEMENT")
    assert role.has_permission("PROCESS_LOANS")
    assert role.has_permission("APPROVE_LOANS")

    assert not role.has_permission("TRANSFER")


def test_administrator_permissions():
    rbac = RBACService()

    role = rbac.get_role("ADMINISTRATOR")

    assert role.has_permission("MANAGE_CUSTOMERS")
    assert role.has_permission("MANAGE_EMPLOYEES")
    assert role.has_permission("MANAGE_BRANCH")
    assert role.has_permission("SYSTEM_ADMIN")

    assert not role.has_permission("DEPOSIT")


def test_user_permission():
    rbac = RBACService()

    user = create_user()
    teller_role = rbac.get_role("TELLER")

    user.assign_role(teller_role)

    assert user.has_permission("VIEW_ACCOUNT")
    assert user.has_permission("DEPOSIT")
    assert user.has_permission("WITHDRAW")

    assert not user.has_permission("TRANSFER")


def test_multiple_roles():
    rbac = RBACService()

    user = create_user()

    teller_role = rbac.get_role("TELLER")
    manager_role = rbac.get_role("MANAGER")

    user.assign_role(teller_role)
    user.assign_role(manager_role)

    assert user.has_permission("DEPOSIT")
    assert user.has_permission("TRANSFER")
    assert user.has_permission("APPROVE_TRANSACTIONS")


def test_authorization_has_permission():
    rbac = RBACService()
    authorization = AuthorizationService()

    user = create_user()
    user.assign_role(rbac.get_role("TELLER"))

    assert authorization.has_permission(
        user,
        "DEPOSIT"
    )

    assert not authorization.has_permission(
        user,
        "TRANSFER"
    )


def test_authorization_check_permission():
    rbac = RBACService()
    authorization = AuthorizationService()

    user = create_user()
    user.assign_role(rbac.get_role("TELLER"))

    assert authorization.check_permission(
        user,
        "DEPOSIT"
    ) is True


def test_authorization_rejects_permission():
    rbac = RBACService()
    authorization = AuthorizationService()

    user = create_user()
    user.assign_role(rbac.get_role("TELLER"))

    try:
        authorization.check_permission(
            user,
            "TRANSFER"
        )

        assert False, "Expected PermissionError"

    except PermissionError as error:
        assert "TRANSFER" in str(error)