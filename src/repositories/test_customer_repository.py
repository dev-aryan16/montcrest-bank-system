print("TEST CUSTOMER REPOSITORY IS RUNNING")
from src.infrastructure.database.database import SessionLocal
from src.repositories.customer_repository import CustomerRepository


def main():
    db = SessionLocal()

    try:
        repository = CustomerRepository(db)

        # 1. Create a customer
        customer = repository.create({
            "first_name": "Test",
            "last_name": "Customer",
            "date_of_birth": "2000-01-01",
            "email": "test.customer@example.com",
            "phone_number": "9000000000",
            "address": "Test Address",
            "status": "ACTIVE"
        })

        print("\nCustomer created:")
        print(customer.customer_id)
        print(customer.first_name)
        print(customer.email)

        # 2. Fetch the same customer
        found_customer = repository.get_by_id(
            customer.customer_id
        )

        print("\nCustomer fetched:")
        print(found_customer.customer_id)
        print(found_customer.first_name)
        print(found_customer.email)

        # 3. Fetch by email
        customer_by_email = repository.get_by_email(
            "test.customer@example.com"
        )

        print("\nCustomer fetched by email:")
        print(customer_by_email.customer_id)
        print(customer_by_email.email)

        # 4. Fetch all customers
        customers = repository.get_all()

        print("\nAll customers:")
        for item in customers:
            print(
                item.customer_id,
                item.first_name,
                item.last_name
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()