from src.infrastructure.database.database import SessionLocal
from src.repositories.customer_repository import CustomerRepository
from src.services.customer_service import CustomerService


def main():

    db = SessionLocal()

    try:
        repository = CustomerRepository(db)
        service = CustomerService(repository)

        customer = service.create_customer({
            "first_name": "Service",
            "last_name": "Test",
            "date_of_birth": "2001-01-01",
            "email": "service.test@example.com",
            "phone_number": "9111111111",
            "address": "Service Test Address",
            "status": "ACTIVE"
        })

        print("\nCustomer created through service:")
        print(customer.customer_id)
        print(customer.first_name)
        print(customer.email)

        found = service.get_customer(
            customer.customer_id
        )

        print("\nCustomer fetched through service:")
        print(found.customer_id)
        print(found.email)

    finally:
        db.close()


if __name__ == "__main__":
    main()