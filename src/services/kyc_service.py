
from src.models.kyc_profile import KYCProfile


class KYCService:

    def create_kyc_profile(
        self,
        customer,
        kyc_id,
        document_type,
        document_number
    ):
        kyc_profile = KYCProfile(
            kyc_id=kyc_id,
            customer=customer,
            document_type=document_type,
            document_number=document_number
        )

        customer.kyc_profile = kyc_profile

        return kyc_profile

    def verify_kyc(self, customer):
        if customer.kyc_profile is None:
            return False

        customer.kyc_profile.verify()
        customer.status = "ACTIVE"

        return True

    def reject_kyc(self, customer):
        if customer.kyc_profile is None:
            return False

        customer.kyc_profile.reject()
        customer.status = "INACTIVE"

        return True

    def get_kyc_status(self, customer):
        if customer.kyc_profile is None:
            return None

        return customer.kyc_profile.status