from datetime import datetime, UTC

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class AccountDB(Base):
    __tablename__ = "accounts"

    account_number: Mapped[int] = mapped_column(
        primary_key=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id"),
        nullable=False,
        index=True
    )

    balance: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0
    )

    account_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    customer = relationship(
        "CustomerDB",
        back_populates="accounts"
    )