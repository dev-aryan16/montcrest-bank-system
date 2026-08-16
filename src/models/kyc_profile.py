from datetime import datetime


class KYCProfile:

    def __init__(
        self,
        kyc_id,
        customer,
        document_type,
        document_number,
        status="PENDING",
        verified_at=None
    ):
        self.kyc_id = kyc_id
        self.customer = customer
        self.document_type = document_type
        self.document_number = document_number
        self.status = status
        self.verified_at = verified_at

    def verify(self):
        self.status = "VERIFIED"
        self.verified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def reject(self):
        self.status = "REJECTED"
        self.verified_at = None

    def get_kyc_info(self):
        return {
            "kyc_id": self.kyc_id,
            "customer": self.customer.get_full_name(),
            "document_type": self.document_type,
            "document_number": self.document_number,
            "status": self.status,
            "verified_at": self.verified_at
        }