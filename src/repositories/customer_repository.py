from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.customer_model import CustomerDB


class CustomerRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, customer_data):
        customer = CustomerDB(
            first_name=customer_data["first_name"],
            last_name=customer_data["last_name"],
            date_of_birth=customer_data["date_of_birth"],
            email=customer_data["email"],
            phone_number=customer_data["phone_number"],
            address=customer_data["address"],
            status=customer_data.get("status", "INACTIVE")
        )

        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)

        return customer

    def get_by_id(self, customer_id):
        statement = select(CustomerDB).where(
            CustomerDB.customer_id == customer_id
        )

        return self.session.scalar(statement)

    def get_by_email(self, email):
        statement = select(CustomerDB).where(
            CustomerDB.email == email
        )

        return self.session.scalar(statement)

    def get_all(self):
        statement = select(CustomerDB).order_by(
            CustomerDB.customer_id
        )

        return self.session.scalars(statement).all()

    def update(self, customer):
        self.session.commit()
        self.session.refresh(customer)

        return customer

    def delete(self, customer_id):
        customer = self.get_by_id(customer_id)

        if customer is None:
            return False

        self.session.delete(customer)
        self.session.commit()

        return True