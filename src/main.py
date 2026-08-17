import os

from models.customer import Customer
from models.bank import Bank
from models.beneficiary import Beneficiary
from models.user import User
from models.permission import Permission
from models.role import Role

from services.transaction_service import TransactionService
from services.account_service import AccountService
from services.transfer_service import TransferService
from services.beneficiary_service import BeneficiaryService
from services.kyc_service import KYCService
from services.authentication_service import AuthenticationService
from services.authorization_service import AuthorizationService
from services.employee_service import EmployeeService
from services.rbac_service import RBACService


# ============================================================
# BANK
# ============================================================

bank1 = Bank(
    bank_id=1,
    bank_name="Montcrest Bank"
)


# ============================================================
# CUSTOMERS
# ============================================================

customer1 = Customer(
    customer_id=101,
    first_name="Aryan",
    last_name="Srivastava",
    date_of_birth="2003-05-15",
    email="aryan@example.com",
    phone_number="9876543210",
    address="Gorakhpur, Uttar Pradesh"
)

bank1.add_customer(customer1)


customer2 = Customer(
    customer_id=102,
    first_name="Rahul",
    last_name="Sharma",
    date_of_birth="2002-08-20",
    email="rahul@example.com",
    phone_number="9123456780",
    address="Lucknow, Uttar Pradesh"
)

bank1.add_customer(customer2)


# ============================================================
# SERVICES
# ============================================================

account_service = AccountService(bank1)
transaction_service = TransactionService(bank1)
transfer_service = TransferService(bank1)
beneficiary_service = BeneficiaryService()
kyc_service = KYCService()
authentication_service = AuthenticationService()
authorization_service = AuthorizationService()
employee_service = EmployeeService()
rbac_service = RBACService()


# ============================================================
# KYC
# ============================================================

print("\n========== KYC WORKFLOW ==========")

kyc_profile = kyc_service.create_kyc_profile(
    customer=customer1,
    kyc_id="KYC1001",
    document_type="AADHAAR",
    document_number="XXXX-XXXX-1234"
)

print("\nKYC Profile:")
print(kyc_profile.get_kyc_info())

verification_result = kyc_service.verify_kyc(customer1)

print("\nKYC Verification Successful:", verification_result)
print("Customer 1:")
print(customer1.get_customer_info())


# ============================================================
# ACCOUNT CREATION
# ============================================================

print("\n========== ACCOUNT CREATION ==========")

savings_account = account_service.create_account(
    customer=customer1,
    account_type="SAVINGS",
    initial_balance=50000
)

current_account = account_service.create_account(
    customer=customer1,
    account_type="CURRENT",
    initial_balance=100000
)

fixed_deposit_account = account_service.create_account(
    customer=customer1,
    account_type="FIXED_DEPOSIT",
    initial_balance=200000
)

customer2_savings_account = account_service.create_account(
    customer=customer2,
    account_type="SAVINGS",
    initial_balance=25000
)


# ============================================================
# INTEREST / POLYMORPHISM
# ============================================================

print("\n========== INTEREST CALCULATION ==========")

accounts = [
    savings_account,
    current_account,
    fixed_deposit_account,
    customer2_savings_account
]

for account in accounts:
    print(
        account.account_type,
        account.account_number,
        "Interest:",
        account.calculate_interest()
    )


# ============================================================
# DEPOSIT
# ============================================================

print("\n========== DEPOSIT ==========")

deposit_transaction = transaction_service.process_deposit(
    savings_account,
    10000
)

print(deposit_transaction.get_transaction_info())


# ============================================================
# WITHDRAWAL
# ============================================================

print("\n========== WITHDRAWAL ==========")

withdrawal_transaction = transaction_service.process_withdrawal(
    savings_account,
    5000
)

print(withdrawal_transaction.get_transaction_info())


# ============================================================
# BENEFICIARY
# ============================================================

print("\n========== BENEFICIARY ==========")

beneficiary1 = Beneficiary(
    beneficiary_id=1,
    owner_customer=customer1,
    beneficiary_name=customer2.get_full_name(),
    account_number=customer2_savings_account.account_number,
    bank_name="Montcrest Bank",
    nickname="Rahul",
    status="ACTIVE",
    created_at="2026-08-15"
)

beneficiary_service.add_beneficiary(
    customer1,
    beneficiary1
)

print(beneficiary1.get_beneficiary_info())


# ============================================================
# TRANSFER
# ============================================================

print("\n========== TRANSFER ==========")

print(
    "Customer 1 Balance Before:",
    savings_account.get_balance()
)

print(
    "Customer 2 Balance Before:",
    customer2_savings_account.get_balance()
)

transfer_transaction = transfer_service.transfer(
    source_account=savings_account,
    destination_account=customer2_savings_account,
    amount=10000
)

print("\nTransfer Transaction:")
print(transfer_transaction.get_transaction_info())

print(
    "Customer 1 Balance After:",
    savings_account.get_balance()
)

print(
    "Customer 2 Balance After:",
    customer2_savings_account.get_balance()
)


# ============================================================
# CUSTOMER USER + AUTHENTICATION
# ============================================================

print("\n========== CUSTOMER AUTHENTICATION ==========")

demo_user_password = os.getenv("DEMO_USER_PASSWORD")

if not demo_user_password:
    raise RuntimeError(
        "DEMO_USER_PASSWORD is not set in the environment."
    )

password_hash = authentication_service.hash_password(
    demo_user_password
)

user1 = User(
    user_id=1,
    username="aryan",
    password_hash=password_hash,
    customer=customer1,
    status="INACTIVE"
)


# Create customer role
customer_role = rbac_service.get_role("CUSTOMER")

if customer_role:
    user1.assign_role(customer_role)

print("\nCustomer User:")
print(user1.get_user_info())


session = authentication_service.authenticate(
    user=user1,
    password=demo_user_password
)

if session:
    print("\nLogin Successful:")
    print(session.get_session_info())

    print(
        "TRANSFER permission:",
        authorization_service.has_permission(
            user1,
            "TRANSFER"
        )
    )


# ============================================================
# EMPLOYEE ROLES
# ============================================================

print("\n========== EMPLOYEE RBAC ==========")

teller_role = rbac_service.get_role("TELLER")
manager_role = rbac_service.get_role("MANAGER")
loan_officer_role = rbac_service.get_role("LOAN_OFFICER")
administrator_role = rbac_service.get_role("ADMINISTRATOR")


# ============================================================
# CREATE EMPLOYEES
# ============================================================

print("\n========== CREATE EMPLOYEES ==========")

teller = employee_service.create_employee(
    employee_type="TELLER",
    first_name="Neha",
    last_name="Verma",
    email="neha@montcrest.com",
    phone_number="9000000001",
    branch="Gorakhpur Main Branch",
    cash_drawer_id="CD-001"
)

manager = employee_service.create_employee(
    employee_type="MANAGER",
    first_name="Amit",
    last_name="Gupta",
    email="amit@montcrest.com",
    phone_number="9000000002",
    branch="Gorakhpur Main Branch",
    approval_limit=500000
)

loan_officer = employee_service.create_employee(
    employee_type="LOAN_OFFICER",
    first_name="Priya",
    last_name="Singh",
    email="priya@montcrest.com",
    phone_number="9000000003",
    branch="Gorakhpur Main Branch",
    specialization="Home Loans"
)

administrator = employee_service.create_employee(
    employee_type="ADMINISTRATOR",
    first_name="Vikas",
    last_name="Mishra",
    email="vikas@montcrest.com",
    phone_number="9000000004",
    branch="Head Office",
    access_level="FULL"
)


# ============================================================
# CREATE EMPLOYEE USERS
# ============================================================

teller_password = os.getenv("TELLER_PASSWORD")
manager_password = os.getenv("MANAGER_PASSWORD")
loan_officer_password = os.getenv("LOAN_OFFICER_PASSWORD")
admin_password = os.getenv("ADMIN_PASSWORD")

required_passwords = {
    "TELLER_PASSWORD": teller_password,
    "MANAGER_PASSWORD": manager_password,
    "LOAN_OFFICER_PASSWORD": loan_officer_password,
    "ADMIN_PASSWORD": admin_password
}

missing_passwords = [
    name
    for name, value in required_passwords.items()
    if not value
]

if missing_passwords:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing_passwords)
    )

teller_password_hash = authentication_service.hash_password(
    teller_password
)

manager_password_hash = authentication_service.hash_password(
    manager_password
)

loan_officer_password_hash = authentication_service.hash_password(
    loan_officer_password
)

admin_password_hash = authentication_service.hash_password(
    admin_password
)


teller_user = employee_service.create_employee_user(
    employee=teller,
    username="neha.teller",
    password_hash=teller_password_hash,
    role=teller_role
)

manager_user = employee_service.create_employee_user(
    employee=manager,
    username="amit.manager",
    password_hash=manager_password_hash,
    role=manager_role
)

loan_officer_user = employee_service.create_employee_user(
    employee=loan_officer,
    username="priya.loan",
    password_hash=loan_officer_password_hash,
    role=loan_officer_role
)

administrator_user = employee_service.create_employee_user(
    employee=administrator,
    username="vikas.admin",
    password_hash=admin_password_hash,
    role=administrator_role
)


# ============================================================
# DISPLAY EMPLOYEES
# ============================================================

print("\n========== EMPLOYEES ==========")

for employee in employee_service.get_all_employees():
    print(employee.get_employee_info())


# ============================================================
# DISPLAY EMPLOYEE USERS
# ============================================================

print("\n========== EMPLOYEE USERS ==========")

for employee_user in employee_service.get_all_users():
    print(employee_user.get_user_info())


# ============================================================
# TEST EMPLOYEE PERMISSIONS
# ============================================================

print("\n========== EMPLOYEE AUTHORIZATION ==========")

print(
    "Teller - DEPOSIT:",
    authorization_service.has_permission(
        teller_user,
        "DEPOSIT"
    )
)

print(
    "Teller - WITHDRAW:",
    authorization_service.has_permission(
        teller_user,
        "WITHDRAW"
    )
)

print(
    "Teller - APPROVE_LOANS:",
    authorization_service.has_permission(
        teller_user,
        "APPROVE_LOANS"
    )
)

print(
    "Manager - APPROVE_LOANS:",
    authorization_service.has_permission(
        manager_user,
        "APPROVE_LOANS"
    )
)

print(
    "Loan Officer - PROCESS_LOANS:",
    authorization_service.has_permission(
        loan_officer_user,
        "PROCESS_LOANS"
    )
)

print(
    "Administrator - SYSTEM_ADMIN:",
    authorization_service.has_permission(
        administrator_user,
        "SYSTEM_ADMIN"
    )
)


# ============================================================
# EMPLOYEE POLYMORPHISM
# ============================================================

print("\n========== EMPLOYEE POLYMORPHISM ==========")

employees = [
    teller,
    manager,
    loan_officer,
    administrator
]

for employee in employees:
    print(employee.get_employee_info())


# ============================================================
# LOGOUT CUSTOMER
# ============================================================

if session:

    logout_result = authentication_service.logout(session)

    print("\n========== CUSTOMER LOGOUT ==========")

    print(
        "Logout Successful:",
        logout_result
    )


# ============================================================
# TRANSACTION HISTORY
# ============================================================

print("\n========== TRANSACTION HISTORY ==========")

for transaction in bank1.transactions:
    print(transaction.get_transaction_info())