from src.models.employee import Employee


class Teller(Employee):

    def __init__(
        self,
        employee_id,
        employee_code,
        first_name,
        last_name,
        email,
        phone_number,
        branch,
        cash_drawer_id,
        status="ACTIVE"
    ):
        super().__init__(
            employee_id=employee_id,
            employee_code=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            designation="TELLER",
            branch=branch,
            status=status
        )

        self.cash_drawer_id = cash_drawer_id

    def handle_deposit(self, amount):
        return f"{self.get_full_name()} processed a deposit of {amount}"

    def handle_withdrawal(self, amount):
        return f"{self.get_full_name()} processed a withdrawal of {amount}"

    def get_employee_info(self):
        info = super().get_employee_info()
        info["cash_drawer_id"] = self.cash_drawer_id
        info["employee_type"] = "TELLER"
        return info