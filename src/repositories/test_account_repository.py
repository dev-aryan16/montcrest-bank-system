from src.infrastructure.database.database import SessionLocal
from src.repositories.account_repository import AccountRepository
from src.repositories.customer_repository import CustomerRepository


def main():
    db = SessionLocal()

    try:
        customer_repository = CustomerRepository(db)
        account_repository = AccountRepository(db)

        # Find existing customer
        customer = customer_repository.get_by_id(1)

        if customer is None:
            print("Customer with ID 1 not found.")
            return

        print("\nCustomer:")
        print(customer.customer_id)
        print(customer.first_name)
        print(customer.last_name)

        # Create an account
        account = account_repository.create({
            "account_number": 1000001,
            "customer_id": customer.customer_id,
            "balance": 50000,
            "account_type": "SAVINGS",
            "status": "ACTIVE"
        })

        print("\nAccount created:")
        print(account.account_number)
        print(account.customer_id)
        print(account.balance)
        print(account.account_type)

        # Fetch account
        found_account = account_repository.get_by_account_number(
            1000001
        )

        print("\nAccount fetched:")
        print(found_account.account_number)
        print(found_account.balance)
        print(found_account.account_type)

        # Fetch all accounts for customer
        customer_accounts = account_repository.get_by_customer_id(
            customer.customer_id
        )

        print("\nCustomer accounts:")
        for item in customer_accounts:
            print(
                item.account_number,
                item.account_type,
                item.balance
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()