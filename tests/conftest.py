import pytest
from faker import Faker

from src.infrastructure.database.database import SessionLocal


fake = Faker()


@pytest.fixture
def db_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def customer_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": fake.date_of_birth().strftime("%Y-%m-%d"),
        "email": fake.unique.email(),
        "phone_number": fake.unique.numerify("9#########"),
        "address": fake.address(),
        "status": "ACTIVE"
    }


@pytest.fixture
def second_customer_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": fake.date_of_birth().strftime("%Y-%m-%d"),
        "email": fake.unique.email(),
        "phone_number": fake.unique.numerify("8#########"),
        "address": fake.address(),
        "status": "ACTIVE"
    }