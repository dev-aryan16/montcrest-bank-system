class CustomerService:

    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def create_customer(self, customer_data):
        # Business validation belongs here
        if not customer_data.get("email"):
            raise ValueError("Email is required.")

        if not customer_data.get("phone_number"):
            raise ValueError("Phone number is required.")

        return self.customer_repository.create(customer_data)

    def get_customer(self, customer_id):
        customer = self.customer_repository.get_by_id(
            customer_id
        )

        if customer is None:
            raise ValueError(
                f"Customer {customer_id} not found."
            )

        return customer

    def get_customer_by_email(self, email):
        customer = self.customer_repository.get_by_email(
            email
        )

        if customer is None:
            raise ValueError(
                f"Customer with email {email} not found."
            )

        return customer

    def get_all_customers(self):
        return self.customer_repository.get_all()

    def update_customer(self, customer_id, updates):
        customer = self.get_customer(customer_id)

        for field, value in updates.items():

            if hasattr(customer, field):
                setattr(customer, field, value)

        return self.customer_repository.update(customer)

    def delete_customer(self, customer_id):
        customer = self.get_customer(customer_id)

        deleted = self.customer_repository.delete(
            customer.customer_id
        )

        if not deleted:
            raise ValueError(
                f"Unable to delete customer {customer_id}."
            )

        return True