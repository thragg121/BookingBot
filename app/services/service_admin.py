from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.admin_services import (
    create_service,
    delete_service,
    get_all_services,
    get_service_by_id,
    rename_service,
    toggle_service,
    update_service_duration,
    update_service_price,
)


async def list_services_for_admin(session):
    return await get_all_services(session)


async def get_admin_service(
    session,
    service_id,
):
    return await get_service_by_id(
        session,
        service_id,
    )


async def create_new_service(
    session: AsyncSession,
    name: str,
    description: str | None,
    duration_minutes: int,
    price: Decimal,
):
    return await create_service(
        session=session,
        name=name,
        description=description,
        duration_minutes=duration_minutes,
        price=price,
    )


async def switch_service_status(
    session,
    service_id,
):
    return await toggle_service(
        session,
        service_id,
    )


async def change_service_price(
    session,
    service_id,
    price,
):
    return await update_service_price(
        session,
        service_id,
        price,
    )


async def change_service_duration(
    session,
    service_id,
    duration_minutes,
):
    return await update_service_duration(
        session,
        service_id,
        duration_minutes,
    )


async def rename_admin_service(
    session,
    service_id,
    new_name,
):
    return await rename_service(
        session,
        service_id,
        new_name,
    )


async def delete_admin_service(
    session,
    service_id,
):
    return await delete_service(
        session,
        service_id,
    )
