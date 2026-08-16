import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.base import Base


load_dotenv()

fake = Faker()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is not set in .env"
    )


test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    session = TestSessionLocal()

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