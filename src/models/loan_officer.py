from src.models.employee import Employee


class LoanOfficer(Employee):

    def __init__(
        self,
        employee_id,
        employee_code,
        first_name,
        last_name,
        email,
        phone_number,
        branch,
        specialization,
        status="ACTIVE"
    ):
        super().__init__(
            employee_id=employee_id,
            employee_code=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            designation="LOAN_OFFICER",
            branch=branch,
            status=status
        )

        self.specialization = specialization

    def process_loan_application(self, application_id):
        return (
            f"{self.get_full_name()} is processing "
            f"loan application {application_id}"
        )

    def review_loan(self, application_id):
        return (
            f"{self.get_full_name()} reviewed "
            f"loan application {application_id}"
        )

    def get_employee_info(self):
        info = super().get_employee_info()
        info["specialization"] = self.specialization
        info["employee_type"] = "LOAN_OFFICER"
        return info