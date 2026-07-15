from decimal import Decimal

from sqlalchemy import select

from app.database.database import Database
from app.models.service import Service


DEFAULT_SERVICES = [
    Service(
        name="Haircut",
        description="Classic haircut service.",
        duration_minutes=60,
        price=Decimal("30.00"),
    ),
    Service(
        name="Consultation",
        description="One-to-one consultation.",
        duration_minutes=45,
        price=Decimal("40.00"),
    ),
    Service(
        name="Premium Session",
        description="Extended premium appointment.",
        duration_minutes=90,
        price=Decimal("70.00"),
    ),
]


async def seed_services(database: Database) -> None:
    async with database.session_factory() as session:
        result = await session.execute(
            select(Service.id).limit(1)
        )

        if result.scalar_one_or_none() is not None:
            return

        session.add_all(DEFAULT_SERVICES)
        await session.commit()
