print("TEST FILE IS RUNNING")

from sqlalchemy import text
from src.infrastructure.database.database import engine

print("ENGINE IMPORTED")

with engine.connect() as connection:
    print("CONNECTED TO DATABASE")

    result = connection.execute(
        text("SELECT current_database();")
    )

    print("DATABASE:", result.scalar())