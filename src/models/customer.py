class Customer:

    def __init__(
        self,
        customer_id,
        first_name,
        last_name,
        date_of_birth,
        email,
        phone_number,
        address
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number
        self.address = address

        # Customer lifecycle / KYC state
        self.status = "INACTIVE"
        self.kyc_profile = None

        # Customer relationships
        self.beneficiaries = []

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_email(self, new_email):
        self.email = new_email

    def update_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number

    def update_address(self, new_address):
        self.address = new_address

    def get_customer_info(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "status": self.status,
            "kyc_status": (
                self.kyc_profile.status
                if self.kyc_profile is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            customer_id=data["customer_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=data["date_of_birth"],
            email=data["email"],
            phone_number=data["phone_number"],
            address=data["address"]
        )

    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email