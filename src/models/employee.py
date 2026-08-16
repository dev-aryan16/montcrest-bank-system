class Employee:

    def __init__(
        self,
        employee_id,
        employee_code,
        first_name,
        last_name,
        email,
        phone_number,
        designation,
        branch,
        status="ACTIVE"
    ):
        self.employee_id = employee_id
        self.employee_code = employee_code
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.designation = designation
        self.branch = branch
        self.status = status

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def activate(self):
        self.status = "ACTIVE"

    def deactivate(self):
        self.status = "INACTIVE"

    def suspend(self):
        self.status = "SUSPENDED"

    def get_employee_info(self):
        return {
            "employee_id": self.employee_id,
            "employee_code": self.employee_code,
            "name": self.get_full_name(),
            "email": self.email,
            "phone_number": self.phone_number,
            "designation": self.designation,
            "branch": self.branch,
            "status": self.status
        }