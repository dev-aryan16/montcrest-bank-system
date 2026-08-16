from models.teller import Teller
from models.manager import Manager
from models.loan_officer import LoanOfficer
from models.administrator import Administrator
from models.user import User


class EmployeeService:

    def __init__(self):
        self.employees = []
        self.users = []
        self._employee_counter = 1000
        self._user_counter = 10000

    def create_employee(
        self,
        employee_type,
        first_name,
        last_name,
        email,
        phone_number,
        branch,
        **kwargs
    ):
        self._employee_counter += 1

        employee_id = self._employee_counter
        employee_code = f"EMP{employee_id}"

        employee_type = employee_type.upper()

        if employee_type == "TELLER":
            employee = Teller(
                employee_id=employee_id,
                employee_code=employee_code,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                branch=branch,
                cash_drawer_id=kwargs.get("cash_drawer_id")
            )

        elif employee_type == "MANAGER":
            employee = Manager(
                employee_id=employee_id,
                employee_code=employee_code,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                branch=branch,
                approval_limit=kwargs.get("approval_limit", 0)
            )

        elif employee_type == "LOAN_OFFICER":
            employee = LoanOfficer(
                employee_id=employee_id,
                employee_code=employee_code,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                branch=branch,
                specialization=kwargs.get(
                    "specialization",
                    "General"
                )
            )

        elif employee_type == "ADMINISTRATOR":
            employee = Administrator(
                employee_id=employee_id,
                employee_code=employee_code,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                branch=branch,
                access_level=kwargs.get(
                    "access_level",
                    "STANDARD"
                )
            )

        else:
            raise ValueError(
                f"Unsupported employee type: {employee_type}"
            )

        self.employees.append(employee)

        return employee

    def create_employee_user(
        self,
        employee,
        username,
        password_hash,
        role
    ):
        self._user_counter += 1

        user = User(
            user_id=self._user_counter,
            username=username,
            password_hash=password_hash,
            customer=None,
            status="INACTIVE"
        )

        user.assign_role(role)

        self.users.append(user)

        return user

    def find_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user

        return None

    def activate_employee(self, employee_id):
        employee = self.find_employee(employee_id)

        if employee is None:
            return False

        employee.activate()
        return True

    def deactivate_employee(self, employee_id):
        employee = self.find_employee(employee_id)

        if employee is None:
            return False

        employee.deactivate()
        return True

    def suspend_employee(self, employee_id):
        employee = self.find_employee(employee_id)

        if employee is None:
            return False

        employee.suspend()
        return True

    def get_all_employees(self):
        return self.employees

    def get_all_users(self):
        return self.users