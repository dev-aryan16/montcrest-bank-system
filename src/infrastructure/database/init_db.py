from src.infrastructure.database.database import engine
from src.infrastructure.database.base import Base

from src.infrastructure.database.models import (
    CustomerDB,
    AccountDB,
    TransactionDB,
)


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")