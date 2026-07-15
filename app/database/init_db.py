from app.database.base import Base
from app.database.database import Database
from app.models import Service, User


async def init_database(database: Database) -> None:
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
