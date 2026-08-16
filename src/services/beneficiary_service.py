class BeneficiaryService:

    def add_beneficiary(self, customer, beneficiary):
        customer.beneficiaries.append(beneficiary)
        return True

    def find_beneficiary(self, customer, beneficiary_id):
        for beneficiary in customer.beneficiaries:
            if beneficiary.beneficiary_id == beneficiary_id:
                return beneficiary
        return None

    def deactivate_beneficiary(self, customer, beneficiary_id):
        beneficiary = self.find_beneficiary(customer, beneficiary_id)

        if beneficiary is None:
            return False

        beneficiary.deactivate()
        return True

    def activate_beneficiary(self, customer, beneficiary_id):
        beneficiary = self.find_beneficiary(customer, beneficiary_id)

        if beneficiary is None:
            return False

        beneficiary.activate()
        return True