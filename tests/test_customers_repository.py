from src.repositories.customer_repository import CustomerRepository


def test_create_customer(db_session, customer_data):
    repository = CustomerRepository(db_session)

    customer = repository.create(customer_data)

    assert customer.customer_id is not None
    assert customer.first_name == customer_data["first_name"]
    assert customer.last_name == customer_data["last_name"]
    assert customer.email == customer_data["email"]
    assert customer.phone_number == customer_data["phone_number"]
    assert customer.status == "ACTIVE"


def test_get_customer_by_id(db_session, customer_data):
    repository = CustomerRepository(db_session)

    customer = repository.create(customer_data)

    found = repository.get_by_id(customer.customer_id)

    assert found is not None
    assert found.customer_id == customer.customer_id
    assert found.email == customer.email


def test_get_customer_by_email(db_session, customer_data):
    repository = CustomerRepository(db_session)

    repository.create(customer_data)

    found = repository.get_by_email(
        customer_data["email"]
    )

    assert found is not None
    assert found.email == customer_data["email"]


def test_get_all_customers(
    db_session,
    customer_data,
    second_customer_data
):
    repository = CustomerRepository(db_session)

    first = repository.create(customer_data)
    second = repository.create(second_customer_data)

    customers = repository.get_all()

    customer_ids = {
        customer.customer_id
        for customer in customers
    }

    assert first.customer_id in customer_ids
    assert second.customer_id in customer_ids