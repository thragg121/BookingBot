from sqlalchemy.ext.asyncio import AsyncSession

from app.database.bookings import (
    delete_user_booking,
    get_user_bookings,
)
from app.database.services import get_active_services


async def list_available_services(
    session: AsyncSession,
):
    return await get_active_services(session)


async def list_user_bookings(
    session: AsyncSession,
    user_id: int,
):
    return await get_user_bookings(
        session=session,
        user_id=user_id,
    )


async def cancel_user_booking(
    session: AsyncSession,
    booking_id: int,
    user_id: int,
):
    return await delete_user_booking(
        session=session,
        booking_id=booking_id,
        user_id=user_id,
    )
