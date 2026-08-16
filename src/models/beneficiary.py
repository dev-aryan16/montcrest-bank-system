class Beneficiary:

    def __init__(
        self,
        beneficiary_id,
        owner_customer,
        beneficiary_name,
        account_number,
        bank_name,
        nickname,
        status,
        created_at
    ):
        self.beneficiary_id = beneficiary_id
        self.owner_customer = owner_customer
        self.beneficiary_name = beneficiary_name
        self.account_number = account_number
        self.bank_name = bank_name
        self.nickname = nickname
        self.status = status
        self.created_at = created_at

    def get_beneficiary_info(self):
        return {
            "beneficiary_id": self.beneficiary_id,
            "owner_customer": self.owner_customer.get_full_name(),
            "beneficiary_name": self.beneficiary_name,
            "account_number": self.account_number,
            "bank_name": self.bank_name,
            "nickname": self.nickname,
            "status": self.status,
            "created_at": self.created_at
        }

    def activate(self):
        self.status = "ACTIVE"

    def deactivate(self):
        self.status = "INACTIVE"