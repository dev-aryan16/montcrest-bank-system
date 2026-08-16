from src.models.employee import Employee
from src.models.teller import Teller
from src.models.manager import Manager
from src.models.loan_officer import LoanOfficer
from src.models.administrator import Administrator


def test_employee_creation():
    employee = Employee(
        employee_id=1,
        employee_code="EMP001",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="9000000001",
        designation="EMPLOYEE",
        branch="Gorakhpur",
        status="ACTIVE"
    )

    assert employee.employee_id == 1
    assert employee.employee_code == "EMP001"
    assert employee.get_full_name() == "John Doe"
    assert employee.status == "ACTIVE"


def test_employee_status_changes():
    employee = Employee(
        employee_id=2,
        employee_code="EMP002",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone_number="9000000002",
        designation="EMPLOYEE",
        branch="Gorakhpur"
    )

    employee.deactivate()
    assert employee.status == "INACTIVE"

    employee.activate()
    assert employee.status == "ACTIVE"

    employee.suspend()
    assert employee.status == "SUSPENDED"


def test_teller():
    teller = Teller(
        employee_id=3,
        employee_code="TEL001",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        phone_number="9000000003",
        branch="Gorakhpur",
        cash_drawer_id="DRAWER001"
    )

    assert isinstance(teller, Employee)
    assert teller.designation == "TELLER"
    assert teller.cash_drawer_id == "DRAWER001"

    assert (
        teller.handle_deposit(5000)
        == "Alice Smith processed a deposit of 5000"
    )

    assert (
        teller.handle_withdrawal(2000)
        == "Alice Smith processed a withdrawal of 2000"
    )

    info = teller.get_employee_info()

    assert info["employee_type"] == "TELLER"
    assert info["cash_drawer_id"] == "DRAWER001"


def test_manager():
    manager = Manager(
        employee_id=4,
        employee_code="MGR001",
        first_name="Robert",
        last_name="Brown",
        email="robert.brown@example.com",
        phone_number="9000000004",
        branch="Gorakhpur",
        approval_limit=100000
    )

    assert isinstance(manager, Employee)
    assert manager.designation == "MANAGER"
    assert manager.approval_limit == 100000

    assert (
        "approved"
        in manager.approve_transaction(50000)
    )

    assert (
        "exceeds approval limit"
        in manager.approve_transaction(150000)
    )

    assert (
        "approved"
        in manager.approve_loan(50000)
    )

    assert (
        "exceeds approval limit"
        in manager.approve_loan(150000)
    )

    info = manager.get_employee_info()

    assert info["employee_type"] == "MANAGER"
    assert info["approval_limit"] == 100000


def test_loan_officer():
    officer = LoanOfficer(
        employee_id=5,
        employee_code="LO001",
        first_name="David",
        last_name="Wilson",
        email="david.wilson@example.com",
        phone_number="9000000005",
        branch="Gorakhpur",
        specialization="Home Loans"
    )

    assert isinstance(officer, Employee)
    assert officer.designation == "LOAN_OFFICER"
    assert officer.specialization == "Home Loans"

    assert (
        officer.process_loan_application("LOAN001")
        == "David Wilson is processing loan application LOAN001"
    )

    assert (
        officer.review_loan("LOAN001")
        == "David Wilson reviewed loan application LOAN001"
    )

    info = officer.get_employee_info()

    assert info["employee_type"] == "LOAN_OFFICER"
    assert info["specialization"] == "Home Loans"


def test_administrator():
    administrator = Administrator(
        employee_id=6,
        employee_code="ADM001",
        first_name="Sarah",
        last_name="Miller",
        email="sarah.miller@example.com",
        phone_number="9000000006",
        branch="Gorakhpur",
        access_level="FULL"
    )

    assert isinstance(administrator, Employee)
    assert administrator.designation == "ADMINISTRATOR"
    assert administrator.access_level == "FULL"

    assert (
        administrator.manage_employee(10)
        == "Administrator managing employee 10"
    )

    assert (
        administrator.manage_branch("Lucknow")
        == "Administrator managing branch Lucknow"
    )

    info = administrator.get_employee_info()

    assert info["employee_type"] == "ADMINISTRATOR"
    assert info["access_level"] == "FULL"