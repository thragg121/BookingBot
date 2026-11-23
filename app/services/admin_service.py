from sqlalchemy.ext.asyncio import AsyncSession

from app.core.texts import format_date_full, mask_name
from app.database.bookings import (
    count_bookings,
    count_today_bookings,
    get_upcoming_bookings,
)
from app.database.users import count_users, get_all_users


async def get_statistics_text(
    session: AsyncSession,
) -> str:
    users_count = await count_users(session)
    bookings_count = await count_bookings(session)
    today_bookings_count = await count_today_bookings(session)

    return (
        "📊 <b>Статистика</b>\n\n"
        f"👥 Клієнтів у базі: <b>{users_count}</b>\n"
        f"📅 Усього записів: <b>{bookings_count}</b>\n"
        f"🗓 Записів на сьогодні: <b>{today_bookings_count}</b>"
    )


async def get_clients_text(
    session: AsyncSession,
    anonymize: bool = False,
) -> str:
    users = await get_all_users(session)

    if not users:
        return "Клієнтів поки немає."

    lines = ["👥 <b>Клієнти</b>"]

    if anonymize:
        lines.append("<i>У демо імена приховані.</i>")

    for user in users[:20]:
        if anonymize:
            lines.append(f"\n• {mask_name(user.first_name)}")
            continue

        username = (
            f"@{user.username}" if user.username else "без username"
        )
        lines.append(
            f"\n<b>{user.first_name}</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"Username: {username}"
        )

    if len(users) > 20:
        lines.append(f"\n\nПоказано 20 з {len(users)} клієнтів.")

    return "\n".join(lines)


async def get_schedule_text(
    session: AsyncSession,
    anonymize: bool = False,
) -> str:
    bookings = await get_upcoming_bookings(session)

    if not bookings:
        return "🗓 Найближчих записів немає."

    lines = ["🗓 <b>Розклад</b>\n"]

    current_date = None

    for booking, service in bookings:
        if booking.booking_date != current_date:
            current_date = booking.booking_date
            lines.append(f"\n<b>{format_date_full(current_date)}</b>")

        client = (
            "клієнт"
            if anonymize
            else f"клієнт <code>{booking.user_id}</code>"
        )
        lines.append(
            f"• {booking.booking_time.strftime('%H:%M')} — "
            f"{service.name} ({client})"
        )

    return "\n".join(lines)
