from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service


async def get_all_services(
    session: AsyncSession,
) -> list[Service]:
    result = await session.execute(
        select(Service).order_by(Service.id)
    )

    return list(result.scalars().all())


async def get_service_by_id(
    session: AsyncSession,
    service_id: int,
) -> Service | None:
    result = await session.execute(
        select(Service).where(
            Service.id == service_id
        )
    )

    return result.scalar_one_or_none()


async def create_service(
    session: AsyncSession,
    name: str,
    description: str | None,
    duration_minutes: int,
    price: Decimal,
) -> Service:

    service = Service(
        name=name,
        description=description,
        duration_minutes=duration_minutes,
        price=price,
        is_active=True,
    )

    session.add(service)

    await session.commit()
    await session.refresh(service)

    return service


async def update_service_price(
    session: AsyncSession,
    service_id: int,
    price: Decimal,
) -> Service | None:

    service = await get_service_by_id(
        session,
        service_id,
    )

    if service is None:
        return None

    service.price = price

    await session.commit()
    await session.refresh(service)

    return service


async def update_service_duration(
    session: AsyncSession,
    service_id: int,
    duration_minutes: int,
) -> Service | None:

    service = await get_service_by_id(
        session,
        service_id,
    )

    if service is None:
        return None

    service.duration_minutes = duration_minutes

    await session.commit()
    await session.refresh(service)

    return service


async def rename_service(
    session: AsyncSession,
    service_id: int,
    new_name: str,
) -> Service | None:

    service = await get_service_by_id(
        session,
        service_id,
    )

    if service is None:
        return None

    service.name = new_name

    await session.commit()
    await session.refresh(service)

    return service


async def toggle_service(
    session: AsyncSession,
    service_id: int,
) -> bool:

    service = await get_service_by_id(
        session,
        service_id,
    )

    if service is None:
        return False

    service.is_active = not service.is_active

    await session.commit()

    return True


async def delete_service(
    session: AsyncSession,
    service_id: int,
) -> bool:

    service = await get_service_by_id(
        session,
        service_id,
    )

    if service is None:
        return False

    await session.delete(service)

    await session.commit()

    return True
