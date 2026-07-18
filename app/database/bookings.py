from datetime import date, datetime, time, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.service import Service


async def create_booking(
    session: AsyncSession,
    user_id: int,
    service_id: int,
    booking_date: date,
    booking_time: time,
) -> Booking | None:
    service_result = await session.execute(
        select(Service).where(
            Service.id == service_id
        )
    )
    service = service_result.scalar_one_or_none()

    if service is None:
        return None

    existing_result = await session.execute(
        select(Booking, Service)
        .join(
            Service,
            Booking.service_id == Service.id,
        )
        .where(
            Booking.booking_date == booking_date
        )
    )

    requested_start = datetime.combine(
        booking_date,
        booking_time,
    )
    requested_end = requested_start + timedelta(
        minutes=service.duration_minutes
    )

    for existing_booking, existing_service in existing_result.all():
        existing_start = datetime.combine(
            existing_booking.booking_date,
            existing_booking.booking_time,
        )
        existing_end = existing_start + timedelta(
            minutes=existing_service.duration_minutes
        )

        overlaps = (
            requested_start < existing_end
            and requested_end > existing_start
        )

        if overlaps:
            return None

    booking = Booking(
        user_id=user_id,
        service_id=service_id,
        booking_date=booking_date,
        booking_time=booking_time,
    )

    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    return booking


async def get_booked_intervals(
    session: AsyncSession,
    booking_date: date,
) -> list[tuple[str, int]]:
    result = await session.execute(
        select(Booking, Service)
        .join(
            Service,
            Booking.service_id == Service.id,
        )
        .where(
            Booking.booking_date == booking_date
        )
    )

    return [
        (
            booking.booking_time.strftime("%H:%M"),
            service.duration_minutes,
        )
        for booking, service in result.all()
    ]


async def get_user_bookings(
    session: AsyncSession,
    user_id: int,
):
    result = await session.execute(
        select(Booking, Service)
        .join(
            Service,
            Booking.service_id == Service.id,
        )
        .where(Booking.user_id == user_id)
        .order_by(
            Booking.booking_date.asc(),
            Booking.booking_time.asc(),
        )
    )

    return result.all()


async def delete_user_booking(
    session: AsyncSession,
    booking_id: int,
    user_id: int,
):
    result = await session.execute(
        select(Booking, Service)
        .join(
            Service,
            Booking.service_id == Service.id,
        )
        .where(
            Booking.id == booking_id,
            Booking.user_id == user_id,
        )
    )

    booking_data = result.one_or_none()

    if booking_data is None:
        return None

    booking, service = booking_data

    booking_snapshot = Booking(
        id=booking.id,
        user_id=booking.user_id,
        service_id=booking.service_id,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        created_at=booking.created_at,
    )

    await session.delete(booking)
    await session.commit()

    return booking_snapshot, service


async def count_bookings(
    session: AsyncSession,
) -> int:
    result = await session.execute(
        select(func.count(Booking.id))
    )

    return int(result.scalar_one())


async def count_today_bookings(
    session: AsyncSession,
) -> int:
    result = await session.execute(
        select(func.count(Booking.id)).where(
            Booking.booking_date == date.today()
        )
    )

    return int(result.scalar_one())


async def get_upcoming_bookings(
    session: AsyncSession,
    limit: int = 30,
):
    result = await session.execute(
        select(Booking, Service)
        .join(
            Service,
            Booking.service_id == Service.id,
        )
        .where(
            Booking.booking_date >= date.today()
        )
        .order_by(
            Booking.booking_date.asc(),
            Booking.booking_time.asc(),
        )
        .limit(limit)
    )

    return result.all()
