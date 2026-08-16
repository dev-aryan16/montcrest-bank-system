from src.models.employee import Employee


class Manager(Employee):

    def __init__(
        self,
        employee_id,
        employee_code,
        first_name,
        last_name,
        email,
        phone_number,
        branch,
        approval_limit,
        status="ACTIVE"
    ):
        super().__init__(
            employee_id=employee_id,
            employee_code=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            designation="MANAGER",
            branch=branch,
            status=status
        )

        self.approval_limit = approval_limit

    def approve_transaction(self, amount):
        if amount <= self.approval_limit:
            return f"Transaction of {amount} approved by {self.get_full_name()}"

        return f"Transaction of {amount} exceeds approval limit"

    def approve_loan(self, loan_amount):
        if loan_amount <= self.approval_limit:
            return f"Loan of {loan_amount} approved by {self.get_full_name()}"

        return f"Loan of {loan_amount} exceeds approval limit"

    def get_employee_info(self):
        info = super().get_employee_info()
        info["approval_limit"] = self.approval_limit
        info["employee_type"] = "MANAGER"
        return info