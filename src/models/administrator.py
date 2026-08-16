from src.models.employee import Employee


class Administrator(Employee):

    def __init__(
        self,
        employee_id,
        employee_code,
        first_name,
        last_name,
        email,
        phone_number,
        branch,
        access_level,
        status="ACTIVE"
    ):
        super().__init__(
            employee_id=employee_id,
            employee_code=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            designation="ADMINISTRATOR",
            branch=branch,
            status=status
        )

        self.access_level = access_level

    def manage_employee(self, employee_id):
        return f"Administrator managing employee {employee_id}"

    def manage_branch(self, branch):
        return f"Administrator managing branch {branch}"

    def get_employee_info(self):
        info = super().get_employee_info()
        info["access_level"] = self.access_level
        info["employee_type"] = "ADMINISTRATOR"
        return info