from sqlalchemy.ext.asyncio import AsyncSession

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
        "📊 <b>BookingBot Statistics</b>\n\n"
        f"👥 Registered users: <b>{users_count}</b>\n"
        f"📅 Total bookings: <b>{bookings_count}</b>\n"
        f"🗓 Today's bookings: <b>{today_bookings_count}</b>"
    )


async def get_clients_text(
    session: AsyncSession,
) -> str:
    users = await get_all_users(session)

    if not users:
        return "No registered clients yet."

    lines = ["👥 <b>Registered Clients</b>\n"]

    for user in users[:20]:
        username = (
            f"@{user.username}"
            if user.username
            else "No username"
        )

        lines.append(
            f"\n<b>{user.first_name}</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"Username: {username}"
        )

    if len(users) > 20:
        lines.append(
            f"\n\nShowing 20 of {len(users)} clients."
        )

    return "\n".join(lines)


async def get_schedule_text(
    session: AsyncSession,
) -> str:
    bookings = await get_upcoming_bookings(session)

    if not bookings:
        return "🗓 No upcoming bookings."

    lines = ["🗓 <b>Upcoming Schedule</b>\n"]

    current_date = None

    for booking, service in bookings:
        if booking.booking_date != current_date:
            current_date = booking.booking_date
            lines.append(
                f"\n<b>{current_date.strftime('%A, %d %B %Y')}</b>"
            )

        lines.append(
            f"• {booking.booking_time.strftime('%H:%M')} — "
            f"{service.name}\n"
            f"  Client ID: <code>{booking.user_id}</code>"
        )

    return "\n".join(lines)
