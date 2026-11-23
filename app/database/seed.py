from decimal import Decimal

from sqlalchemy import select

from app.database.database import Database
from app.models.service import Service


DEFAULT_SERVICES = [
    Service(
        name="Жіноча стрижка",
        description="Стрижка, миття та укладка.",
        duration_minutes=60,
        price=Decimal("600.00"),
    ),
    Service(
        name="Манікюр з покриттям",
        description="Апаратний манікюр + гель-лак.",
        duration_minutes=90,
        price=Decimal("750.00"),
    ),
    Service(
        name="Чоловіча стрижка",
        description="Класична або фейд.",
        duration_minutes=45,
        price=Decimal("400.00"),
    ),
    Service(
        name="Фарбування брів",
        description="Корекція та фарбування.",
        duration_minutes=30,
        price=Decimal("350.00"),
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
