from aiogram import Bot

from config import Config


async def notify_admins_about_booking(
    bot: Bot,
    config: Config,
    user_id: int,
    first_name: str,
    username: str | None,
    booking_id: int,
    service_name: str,
    booking_date: str,
    booking_time: str,
    price: str,
) -> None:
    username_text = (
        f"@{username}"
        if username
        else "Not specified"
    )

    text = (
        "🔔 <b>New Booking</b>\n\n"
        f"Booking ID: <code>{booking_id}</code>\n"
        f"Client: <b>{first_name}</b>\n"
        f"Username: {username_text}\n"
        f"User ID: <code>{user_id}</code>\n\n"
        f"Service: <b>{service_name}</b>\n"
        f"Date: <b>{booking_date}</b>\n"
        f"Time: <b>{booking_time}</b>\n"
        f"Price: <b></b>"
    )

    for admin_id in config.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
            )
        except Exception:
            continue


async def notify_admins_about_cancellation(
    bot: Bot,
    config: Config,
    user_id: int,
    first_name: str,
    username: str | None,
    booking_id: int,
    service_name: str,
    booking_date: str,
    booking_time: str,
) -> None:
    username_text = (
        f"@{username}"
        if username
        else "Not specified"
    )

    text = (
        "❌ <b>Booking Cancelled</b>\n\n"
        f"Booking ID: <code>{booking_id}</code>\n"
        f"Client: <b>{first_name}</b>\n"
        f"Username: {username_text}\n"
        f"User ID: <code>{user_id}</code>\n\n"
        f"Service: <b>{service_name}</b>\n"
        f"Date: <b>{booking_date}</b>\n"
        f"Time: <b>{booking_time}</b>"
    )

    for admin_id in config.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
            )
        except Exception:
            continue
