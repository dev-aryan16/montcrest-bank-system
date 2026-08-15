from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.base import Base


class CustomerDB(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    date_of_birth: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="INACTIVE",
        nullable=False
    )

    accounts = relationship(
        "AccountDB",
        back_populates="customer"
    )
    