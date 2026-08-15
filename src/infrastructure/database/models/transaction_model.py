from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class TransactionDB(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    transaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    source_account: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.account_number"),
        nullable=True
    )

    destination_account: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.account_number"),
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    source = relationship(
        "AccountDB",
        foreign_keys=[source_account]
    )

    destination = relationship(
        "AccountDB",
        foreign_keys=[destination_account]
    )