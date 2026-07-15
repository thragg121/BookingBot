from datetime import date, time

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.bookings import create_booking


async def save_booking(
    session: AsyncSession,
    user_id: int,
    service_id: int,
    booking_date: date,
    booking_time: time,
):
    return await create_booking(
        session,
        user_id,
        service_id,
        booking_date,
        booking_time,
    )
